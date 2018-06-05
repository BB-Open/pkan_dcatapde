# -*- coding: utf-8 -*-
"""Harvesting adapter."""
from DateTime.DateTime import time
from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.constants import HARVESTER_DEFAULT_KEY
from pkan.dcatapde.constants import HARVESTER_DEXTERITY_KEY
from pkan.dcatapde.constants import HARVESTER_ENTITY_KEY
from pkan.dcatapde.constants import MAX_QUERY_PREVIEW_LENGTH
from pkan.dcatapde.constants import RDF_FORMAT_JSONLD
from pkan.dcatapde.constants import RDF_FORMAT_METADATA
from pkan.dcatapde.constants import RDF_FORMAT_TURTLE
from pkan.dcatapde.constants import RDF_FORMAT_XML
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.content.rdfs_literal import literal2plone
from pkan.dcatapde.harvesting.errors import RequiredPredicateMissing
from pkan.dcatapde.harvesting.rdf.interfaces import IRDFJSONLD
from pkan.dcatapde.harvesting.rdf.interfaces import IRDFTTL
from pkan.dcatapde.harvesting.rdf.interfaces import IRDFXML
from pkan.dcatapde.harvesting.rdf.visitors import DCATVisitor
from pkan.dcatapde.harvesting.rdf.visitors import InputVisitor
from pkan.dcatapde.harvesting.rdf.visitors import Node
from pkan.dcatapde.harvesting.rdf.visitors import NS_ERROR
from pkan.dcatapde.harvesting.rdf.visitors import NS_WARNING
from pkan.dcatapde.harvesting.rdf.visitors import NT_DEFAULT
from pkan.dcatapde.harvesting.rdf.visitors import NT_DX_DEFAULT
from pkan.dcatapde.harvesting.rdf.visitors import NT_RESIDUAL
from pkan.dcatapde.harvesting.rdf.visitors import NT_SPARQL
from pkan.dcatapde.harvesting.rdf.visitors import RealRunVisitor
from pkan.dcatapde.log.log import TranslatingFormatter
from pkan.dcatapde.structure.sparql import QUERY_A
from pkan.dcatapde.structure.sparql import QUERY_ATT
from pkan.dcatapde.structure.sparql import QUERY_P
from pkan.dcatapde.structure.structure import IMP_REQUIRED
from pkan.dcatapde.structure.structure import StructDCATCatalog
from pkan.dcatapde.structure.structure import StructDCATDataset
from pkan.dcatapde.structure.structure import StructRDFSLiteral
from pkan.dcatapde.utils import get_available_languages_iso
from pkan.dcatapde.utils import get_available_languages_title
from pkan.dcatapde.utils import get_default_language
from plone import api
from plone.api import content
from plone.api.exc import InvalidParameterError
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import safe_unicode
from plone.memoize import ram
from pyparsing import ParseException
from rdflib import Graph
from rdflib.plugins.memory import IOMemory
from rdflib.term import Literal
from traceback import format_tb
from xml.sax import SAXParseException
from zope.annotation import IAnnotations
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer

import io
import logging
import sys
import vkbeautify as vkb


IFaceToRDFFormatKey = {
    IRDFTTL: RDF_FORMAT_TURTLE,
    IRDFJSONLD: RDF_FORMAT_JSONLD,
    IRDFXML: RDF_FORMAT_XML,
}


def cache_key(func, self):
    """cache key factory for rdf graph. With timeout 300 seconds
    :param func:
    :param self:
    :return:
    """
    key = u'{0}_{1}'.format(
        time() // 300,
        self.harvester.url,
    )
    return key


@adapter(IHarvester)
@implementer(IRDFTTL)
@implementer(IRDFJSONLD)
@implementer(IRDFXML)
class RDFProcessor(object):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    def __init__(self, harvester):
        # remember the harvester
        self.harvester = harvester
        # look if we have a harvesting type adapter
        # try:
        #     self.harvesting_type = \
        #         self.harvester.harvesting_type(self.harvester)
        # except TypeError:
        #     self.harvesting_type = None

        # fetch the preprocessor adapter
        # self.data_cleaner = self.harvester.data_cleaner(self.harvester)
        self.cleaned_data = None
        # self.field_config = get_field_config(self.harvester)
        self.harvesting_context = self.harvester
        if self.harvester:
            if getattr(self.harvester, 'base_object', None):
                self.harvesting_context = content.get(
                    UID=self.harvester.base_object,
                )

        # check which top_node we should use
        if getattr(self.harvester, 'top_node', None) and \
                self.harvester.top_node == CT_DCAT_DATASET:
            self.struct_class = StructDCATDataset
        else:
            self.struct_class = StructDCATCatalog

        # determine the source format serializer string for rdflib from our
        # own interface. Todo this is a bit ugly
        self.rdf_format_key = IFaceToRDFFormatKey[self.harvester.source_type]
        self.rdf_format = RDF_FORMAT_METADATA[self.rdf_format_key]
        self.serialize_format = self.rdf_format['serialize_as']
        self.def_lang = get_default_language()
        self.available_languages = get_available_languages_iso()
        self.all_languages = get_available_languages_title().values()
        self.setup_logger()
        self.get_entity_mapping()

    def get_entity_mapping(self):
        """Fill the mappings for the entities"""
        annotations = IAnnotations(self.harvester)
        self.mapping_sparql = {}
        self.mapping_dexterity = {}
        self.mapping_default = {}
        if HARVESTER_ENTITY_KEY in annotations:
            self.mapping_sparql = annotations[HARVESTER_ENTITY_KEY]
        if HARVESTER_DEXTERITY_KEY in annotations:
            self.mapping_dexterity = annotations[HARVESTER_DEXTERITY_KEY]
        if HARVESTER_DEFAULT_KEY in annotations:
            self.mapping_default = \
                annotations[HARVESTER_DEFAULT_KEY]

    @property
    @ram.cache(cache_key)
    def graph(self):
        """In Memory representation of the incoming RDF graph"""
        rdfstore = IOMemory()
        _graph = Graph(rdfstore)
        _graph.parse(source=self.harvester.url, format=self.serialize_format)
        return _graph

    def setup_logger(self):
        """Log to a io.stream that can later be embedded in the view output"""
        # get a logger named after the serializing format we use
        log = logging.getLogger(self.serialize_format)
        # get and remember the stream
        self.log_stream = io.StringIO()
        # construct a streamhandler
        stream_handler = logging.StreamHandler(self.log_stream)
        # and a formatter for HTML output
        format = '<p>%(asctime)s - %(name)s - %(levelname)s - %(message)s</p>'
        request = getattr(self.harvesting_context, 'REQUEST', None)
        formatter = TranslatingFormatter(format, request=request)
        # and plug things together
        stream_handler.setFormatter(formatter)
        log.addHandler(stream_handler)
        self.log = log

    def top_nodes(self, visitor):
        """Find top nodes: Catalogs or datasets"""

        allowed_types = self.harvesting_context.allowedContentTypes()
        klass = getUtility(IDexterityFTI, name=self.harvester.top_node)

        if klass not in allowed_types:
            msg = '{top} is not allowed in {context}.'.format(
                context=self.harvesting_context,
                top=self.harvester.top_node,
            )
            visitor.scribe.write(
                msg=msg,
                level='error',
            )
            return

        struct = self.struct_class(self.harvester)
        # Get Mapping from the harvester
        if struct.rdf_type in self.harvester.mapper:
            query = self.harvester.mapper[struct.rdf_type]
            bindings = {'o': struct.rdf_type}
        else:
            # Since we have no rdf_parent we have to look for types of nodes
            query = QUERY_A
            bindings = {'o': struct.rdf_type}
        res = self.graph.query(query, initBindings=bindings)

        for top_node in res.bindings:
            yield top_node['s']

    def handle_list(self, visitor, res, **kwargs):
        obj_data = kwargs['obj_data']
        field_name = kwargs['field_name']
        field = kwargs['field']
        context = kwargs['context']
        predicate = field['predicate']
        obj_class = field['object']

        obj_data[field_name] = []
        for i in res.bindings:
            rdf_obj = i['o']
            # If the field is a Literal we simply store it.
            if obj_class == StructRDFSLiteral:
                obj_data[field_name].append(literal2plone(rdf_obj, field))
                visitor.end_node(predicate, obj_class, **kwargs)

            # if not we have to create a sub object recursively
            else:
                node = visitor.end_node(predicate, obj_class, **kwargs)
                visitor.push_node(node)
                sub = self.crawl(
                    visitor,
                    context=context,
                    rdf_node=rdf_obj,
                    target_struct=obj_class,
                )
                if sub:
                    obj_data[field_name].append(sub.UID())

            visitor.scribe.write(
                level='info',
                msg=u'{type} object {obj}: attribute {att}:= {val}',
                val=rdf_obj,
                obj=kwargs['rdf_node'],
                type=kwargs['struct'].rdf_type,
            )

    def handle_dict(self, visitor, res, **kwargs):
        obj_data = kwargs['obj_data']
        field_name = kwargs['field_name']
        field = kwargs['field']
        predicate = field['predicate']
        obj_class = field['object']

        obj_data[field_name] = {}
        for i in res.bindings:
            # special handling of literals without language
            if not ('o1' in i):
                rdf_obj = i['o']
                obj_data[field_name][self.def_lang] = unicode(i['o'])
                visitor.scribe.write(
                    level='info',
                    msg=u'{type} object {obj}: attribute {att}:= {val}',
                    val=rdf_obj,
                    att=field['predicate'],
                    obj=kwargs['rdf_node'],
                    type=kwargs['struct'].rdf_type,
                )
            else:
                lang = i['o1']

                # convert 2-letter-format to 3-letter-format
                if unicode(lang) in self.available_languages:
                    lang = self.available_languages[unicode(lang)]

                elif lang not in self.all_languages:
                    lang = self.def_lang

                obj_data[field_name][lang] = unicode(i['o2'])
                visitor.scribe.write(
                    level='info',
                    msg=u'{type} object {obj}: attribute {att}:= {val}',
                    val=str(i['o1']) + ':' + str(i['o1']),
                    att=predicate,
                    obj=kwargs['rdf_node'],
                    type=kwargs['struct'].rdf_type,
                )

            visitor.end_node(predicate, obj_class, **kwargs)

    def properties(self, visitor, **kwargs):
        """At first we run over the fields and references only, to collect
        the data necessary to construct the CT instance.
        With the contained instances will be dealed if the CT instance
        is constructed"""

        obj_data = kwargs['obj_data']
        context = kwargs['context']

        field_and_references = kwargs['struct'].fields_and_referenced

        for field_name, field in field_and_references.items():

            params = kwargs.copy()
            params['field_name'] = field_name
            params['field'] = field
            params['obj_data'] = obj_data
            params['context'] = context

            self.property(visitor, **params)

    def property(self, visitor, **kwargs):

        field = kwargs['field']
        field_name = kwargs['field_name']
        obj_data = kwargs['obj_data']
        context = kwargs['context']
        predicate = field['predicate']
        obj_class = field['object']

        visitor.scribe.write(
            level='info',
            msg=u'{type} object {obj}: '
                u'searching {imp} attribute {att}',
            att=field['predicate'],
            imp=field['importance'],
            obj=kwargs['rdf_node'],
            type=kwargs['struct'].rdf_type,
        )
        # query for an attibute
        query = QUERY_ATT

        params = kwargs.copy()

        token = kwargs['struct'].field2token(field_name, field)
        if token in self.mapping_dexterity:
            uid = self.mapping_dexterity[token]
            obj = content.get(UID=uid)
            obj_data[field_name] = uid
            params['node_type'] = NT_DX_DEFAULT
            node = visitor.end_node(predicate, obj_class, **params)
            visitor.push_node(node)
            self.crawl_dx(
                visitor,
                context=obj,
                target_struct=field['object'],
            )
            return

        if token in self.mapping_default:
            obj_data[field_name] = self.mapping_default[token]
            params['node_type'] = NT_DEFAULT
            visitor.end_node(predicate, obj_class, **params)
            return

        if token in self.mapping_sparql:
            params['node_type'] = NT_SPARQL
            query = self.mapping_sparql[token]
        # Query the RDF db. Subject is the node we are on
        # Predicate is the attribute we like to find in the RDF
        bindings = {
            's': kwargs['rdf_node'],
            'p': field['predicate'],
        }
        res = self.graph.query(query, initBindings=bindings)

        # Dealing with required fields not delivered
        if len(res) == 0:
            if field['importance'] == IMP_REQUIRED:
                visitor.scribe.write(
                    level='error',
                    msg=u'{type} object {obj}: required '
                        u'attribute {att} not found',
                    att=field['predicate'],
                    obj=kwargs['rdf_node'],
                    type=kwargs['struct'].rdf_type,
                )
                params['status'] = NS_ERROR
                visitor.end_node(predicate, obj_class, **params)
            else:
                visitor.scribe.write(
                    level='warn',
                    msg=u'{type} object {obj}: {imp} '
                        u'attribute {att} not found',
                    att=field['predicate'],
                    imp=field['importance'],
                    obj=kwargs['rdf_node'],
                    type=kwargs['struct'].rdf_type,
                )
                params['status'] = NS_WARNING
                visitor.end_node(predicate, obj_class, **params)
            return
        else:
            # dealing with list like fields
            if field['type'] == list:
                self.handle_list(visitor, res, **params)

            # dealing with dict like fields aka Literals
            elif field['type'] == dict:
                self.handle_dict(visitor, res, **params)
            # Iten/list collision checking. Attribute is Item in DCATapded,
            # but a list is delivered.
            elif len(res) > 1:
                visitor.scribe.write(
                    level='error',
                    msg=u'{type} object {obj}: '
                        u'attribute {att} to many values',
                    att=field['predicate'],
                    obj=kwargs['rdf_node'],
                    type=kwargs['struct'].rdf_type,
                )
                # Todo: Error handling
                return
            # Simple case of a single item
            else:
                # If the field is a Literal we simply store it.
                if field['object'] == StructRDFSLiteral:
                    val = literal2plone(res.bindings[0]['o'], field)
                    obj_data[field_name] = val
                    visitor.end_node(predicate, obj_class, **params)
                # if not we have to create a sub object recursively
                else:
                    node = visitor.end_node(predicate, obj_class, **params)
                    visitor.push_node(node)
                    sub = self.crawl(
                        visitor,
                        context=context,
                        rdf_node=res.bindings[0]['o'],
                        target_struct=field['object'],
                    )
                    if sub:
                        obj_data[field_name] = sub.UID()
                    else:
                        obj_data[field_name] = None
                visitor.scribe.write(
                    level='info',
                    msg=u'{type} object {obj}: attribute {att}:= {val}',
                    val=str(obj_data[field_name]),
                    att=field['predicate'],
                    obj=kwargs['rdf_node'],
                    type=kwargs['struct'].rdf_type,
                )

    def residuals(self, visitor, **kwargs):
        """Here we look for rdf edges that are not in the DCAT-AP.de norm"""

        subject = kwargs['rdf_node']
        kwargs['node_type'] = NT_RESIDUAL

        visitor.scribe.write(
            level='info',
            msg=u'{type} object {obj}: looking for residual properties',
            obj=kwargs['rdf_node'],
            type=kwargs['struct'].rdf_type,
        )
        # Query all predicates
        query = QUERY_P
        # Query the RDF db. Subject is the node we are on
        # is the attribute we like to find in the RDF
        bindings = {
            's': subject,
        }
        results = self.graph.query(query, initBindings=bindings)

        if len(results) > 0:
            visitor.scribe.write(
                level='info',
                msg=u'{type} object {obj}: residual properties found',
                obj=kwargs['rdf_node'],
                type=kwargs['struct'].rdf_type,
            )
        else:
            visitor.scribe.write(
                level='info',
                msg=u'{type} object {obj}: No residual properties found',
                obj=kwargs['rdf_node'],
                type=kwargs['struct'].rdf_type,
            )

        # Find the predicates we have already processed
        field_and_references = kwargs['struct'].fields_and_referenced
        dcat_predicates_values = field_and_references.values()
        dcat_predicates = [i['predicate'] for i in dcat_predicates_values]
        dcat_contained_values = kwargs['struct'].contained.values()
        dcat_contained = [i['predicate'] for i in dcat_contained_values]
        dcat_predicates += dcat_contained

        # Handle the predicates we have missed
        for result in results:
            # if the result is already covered by dcat-ap.de pass
            if result['p'] in dcat_predicates:
                continue
            self.residual(visitor, result, **kwargs)

        visitor.pop_node()

    def residual(self, visitor, predicate_object, **kwargs):
        """Handle on residual"""

        predicate = predicate_object['p']
        rdf_obj = predicate_object['o']

        # If the field is a Literal we simply store it.
        if isinstance(rdf_obj, Literal):
            val = literal2plone(rdf_obj)
            visitor.end_node(predicate, rdf_obj, **kwargs)
        # if not we have to create a sub object recursively
        else:
            params = kwargs.copy()
            params['rdf_node'] = rdf_obj
            node = visitor.end_node(predicate, rdf_obj, **kwargs)
            visitor.push_node(node)
            val = self.residuals(
                visitor,
                **params)
        visitor.scribe.write(
            level='info',
            msg=u'{type} object {obj}: attribute {att}:= {val}',
            val=val,
            att=predicate,
            obj=kwargs['rdf_node'],
            type=kwargs['struct'].rdf_type,
        )

    def contained(self, visitor, **kwargs):
        """At first we run over the fields and references only, to collect
        the data necessary to construct the CT instance.
        With the contained instances will be dealed if the CT instance
        is constructed"""

        struct = kwargs['struct']
        rdf_node = kwargs['rdf_node']
        context = kwargs['obj']

        # query for an attibute
        query = QUERY_ATT
        #   Handle the contained objects
        for field_name, field in struct.contained.items():
            # Todo : query the entity mapper
            # if struct.rdf_type in self.harvester.mapper:
            #                query = self.harvester.mapper[struct.rdf_type]
            predicate = field['predicate']
            visitor.scribe.write(
                level='info',
                msg=u'{type} object {obj}: searching contained {att}',
                att=predicate,
                obj=kwargs['rdf_node'],
                type=kwargs['struct'].rdf_type,
            )

            # Query the RDF db. Subject is still the rdf_node
            # Predicate is the attribute we like to find in the RDF
            bindings = {
                's': rdf_node,
                'p': predicate,
            }
            res = self.graph.query(query, initBindings=bindings)

            for i in res.bindings:
                rdf_obj = i['o']
                params = {
                    'field': field,
                    'field_name': field_name,
                    'rdf_node': rdf_obj,
                    'struct': struct,
                }
                node = visitor.end_node(predicate, field['object'], **params)
                visitor.push_node(node)

                self.crawl(
                    visitor,
                    context=context,
                    rdf_node=rdf_obj,
                    target_struct=field['object'],
                )
                visitor.scribe.write(
                    level='info',
                    msg=u'Crawling to sub obj {obj} of type {type} '
                        u'attribute {att}',
                    att=predicate,
                    obj=rdf_obj,
                    type=struct.rdf_type,
                )

    def get_title(self, struct, obj_data):
        # Find a title for the dxobject to be created
        title = None
        for title_field in struct.title_field:
            try:
                all_titles = obj_data[title_field]
                if not all_titles:
                    continue
                if isinstance(all_titles, dict):
                    title = unicode(all_titles.items()[0][1])
                elif isinstance(all_titles, list):
                    title = unicode(all_titles[0])
                else:
                    title = all_titles
            except KeyError:
                continue
        if not title:
            raise RequiredPredicateMissing
        return title

    def checkURI(self, uri):
        catalog = api.portal.get_tool(name='portal_catalog')
        query = {'uri_in_triplestore': uri}
        brains = catalog(query)
        return brains

    def create_dx_obj(
        self,
        visitor,
        struct,
        context,
        rdf_node,
        obj_data,
        title,
    ):
        # check if object should be created
        if not visitor.real_run:
            return None

        # check if the URI of the object is already available as DX object
        brains = self.checkURI(rdf_node.toPython())
        if len(brains) > 0:
            visitor.scribe.write(
                level='warn',
                msg=u'{type} dxobject {obj} reused from {context}',
                context=brains[0].getURL(),
                obj=rdf_node,
                type=struct.rdf_type,
            )
            return brains[0].getObject()

        # Handle not given descriptions to prevent u'None' brains
        desc_found = False
        for desc_field in struct.desc_field:
            if desc_field in obj_data:
                desc_found = True
                break

        if not desc_found:
            for desc_field in struct.desc_field:
                obj_data[desc_field] = None
            obj_data['description'] = None

        # Create an instance of the node as dexterity object
        try:
            obj = content.create(
                context,
                struct.portal_type,
                title=title,
                in_harvester=self.harvester.UID(),
                uri_in_triplestore=rdf_node.toPython(),
                **obj_data)
        # We are not allowed to create the content here
        except InvalidParameterError:
            # So we try it directly under the harvest
            visitor.scribe.write(
                level='warn',
                msg=u'{type} dxobject {obj} created at {context}',
                context=self.harvester.virtual_url_path(),
                obj=rdf_node,
                type=struct.rdf_type,
            )

            obj = content.create(
                self.harvester,
                struct.portal_type,
                title=title,
                in_harvester=self.harvester.UID(),
                uri_in_triplestore=rdf_node.toPython(),
                **obj_data)

        obj.reindexObject()
        visitor.scribe.write(
            level='info',
            msg=u'{type} dxobject {obj} created at {context}',
            context=context.virtual_url_path(),
            obj=rdf_node,
            type=struct.rdf_type,
        )
        return obj

    def crawl(
        self,
        visitor,
        target_struct=None,
        context=None,
        rdf_node=None,
    ):
        """Analyse the RDF structure"""

        # Activate the struct
        struct = target_struct(self.harvester)

        # here we collect the data to generate our DX object
        obj_data = {}

        # set the original URI as rdf_about field:
        obj_data['rdf_about'] = rdf_node

        # Go for the DCAT-AP.de properties of the current node
        self.properties(
            visitor,
            context=context,
            rdf_node=rdf_node,
            struct=struct,
            obj_data=obj_data,
        )

        # # Find the edges that are not included in DCAT-Ap.de
        # self.residuals(
        #     visitor,
        #     context=context,
        #     rdf_node=rdf_node,
        #     struct=struct,
        #     obj_data=obj_data,
        # )

        try:
            # get a title for the dxobject
            title = self.get_title(struct, obj_data)

            # create the DX object
            obj = self.create_dx_obj(
                visitor,
                struct,
                context,
                rdf_node,
                obj_data,
                title,
            )
        except RequiredPredicateMissing:
            if context:
                context_url = context.virtual_url_path()
            else:
                context_url = '/'
            visitor.scribe.write(
                level='error',
                msg=u'{type} dxobject {obj} cannot be created at {context}',
                context=context_url,
                obj=rdf_node,
                type=struct.rdf_type,
            )
            obj = None
            title = None

        # deal with the contained objects
        self.contained(
            visitor,
            context=context,
            rdf_node=rdf_node,
            struct=struct,
            obj_data=obj_data,
            obj=obj,
        )

        # end recursion
        node = visitor.pop_node()

        node.title = title

        return obj

    def crawl_dx(
        self,
        visitor,
        target_struct=None,
        context=None,
        rdf_node=None,
    ):

        struct = target_struct(context)
        field_and_references = struct.fields_and_referenced
        obj_data = {}

        for field_name, field in field_and_references.items():
            predicate = field['predicate']
            obj_class = field['object']
            params = {
                'field': field,
                'field_name': field_name,
                'struct': target_struct,
            }
            # If the field is a Literal we simply store it.
            if obj_class == StructRDFSLiteral:
                # todo: is None as default correct or should
                # this case be ignored
                obj_data[field_name] = getattr(context, field_name, None)
                visitor.end_node(predicate, obj_class, **params)
            # if not we have to create a sub object recursively
            else:
                node = visitor.end_node(predicate, obj_class, **params)
                visitor.push_node(node)
                sub = self.crawl_dx(
                    visitor,
                    context=context,
                    target_struct=obj_class,
                )
                obj_data[field_name] = sub
            visitor.scribe.write(
                level='info',
                msg=u'{type} DX object {obj}: attribute {att}:= {val}',
                val=obj_data[field_name],
                att=predicate,
                obj=context,
                type=struct.rdf_type,
            )

        node = visitor.pop_node()
        # todo: check if this is correct
        if context:
            node.title = context.Title()
        else:
            node.title = ''

    def parse_dcat_data(self):
        """Parsing the data in respect to the dcat ap.de diagram
        """
        self.log.info(u'Parsing for dcat information')
        uri = self.harvester.url

        msg = _(
            u'Reading {kind} file {uri} into rdflib',
            mapping={'kind': self.serialize_format, 'uri': uri},
        )
        self.log.info(msg)

        # self.scribe = Scribe()
        visitor = DCATVisitor()

        # start on the top nodes
        self.top_nodes(visitor)

        self.log.info(u'DCAT parsed successfully')

        return visitor.to_cytoscape()

    def parse_input_data(self):
        """Parsing the data with focus on the input data
        """
        self.log.info(u'Parsing for input information')
        uri = self.harvester.url

        msg = _(
            u'Reading {kind} file {uri} into rdflib',
            mapping={'kind': self.serialize_format, 'uri': uri},
        )
        self.log.info(msg)

        # self.scribe = Scribe()
        visitor = InputVisitor()

        # start on the top nodes
        self.top_nodes(visitor)

        self.log.info(u'Input data parsed successfully')

        for line in visitor.scribe.read():
            self.log.info(line)

        return visitor.to_cytoscape()

    def get_preview(self, query, bindings={}):
        """
        Preview for sparqle_query

        if url and rdf_format are given and different to self.harvester
        we make a temporary graph
        """
        preview = _(u'Result: ')
        try:
            res = self.graph.query(query, initBindings=bindings)
        except ParseException:
            preview += _(u'Wrong Syntax')
        except SAXParseException:
            preview += _(u'Could not read source.')
        except ValueError:
            preview += _(u'Did not find correct parameters to request data.')
        except TypeError:
            preview += _(u'Did not find correct parameters to request data.')
        else:
            preview += safe_unicode(vkb.xml(res.serialize()))
        if preview and len(preview) > MAX_QUERY_PREVIEW_LENGTH:
            preview = preview[:MAX_QUERY_PREVIEW_LENGTH] + '...'
        return preview

    def remove_objects(self):
        # todo: remove in triple store
        uid = self.harvester.UID()
        object_brains = content.find(in_harvester=uid)
        count = len(object_brains)
        for i in range(count):
            try:
                brain = object_brains[i]
                content.delete(obj=brain.getObject())
            except KeyError:
                # object is already deleted because parent was deleted
                continue

    def run(self, top_nodes, visitor):
        """crawl the top nodes"""
        for top_node in top_nodes:
            msg = _(u'Reading {top_node}')
            visitor.scribe.write(
                level='info',
                msg=msg,
                kind=self.serialize_format,
                top_node=top_node,
            )
            struct = self.struct_class(self.harvester)
            args = {
                'structure': struct,
            }
            node = Node(**args)
            visitor.push_node(node)

            self.crawl(
                visitor,
                context=self.harvesting_context,
                rdf_node=top_node,
                target_struct=self.struct_class,
            )
            msg = _(u'Finished reading of {top_node}')
            visitor.scribe.write(
                level='info',
                msg=msg,
                kind=self.serialize_format,
                top_node=top_node,
            )

    def prepare_and_run(self, visitor):
        """Dry Run: Returns Log-Information.
        """
        # Just to have the posibility to reset
        self.harvester._graph = None
        self.harvester._rdfstore = None

        if visitor.real_run:
            msg = u'starting harvest real run'
        else:
            msg = u'starting harvest dry run'
        visitor.scribe.write(
            level='info',
            msg=msg,
        )

        if visitor.real_run:
            msg = 'Removing old objects'
            visitor.scribe.write(
                level='info',
                msg=msg,
            )
            self.remove_objects()

        uri = self.harvester.url

        msg = _(u'Reading {kind} file {uri}')
        visitor.scribe.write(
            level='info',
            msg=msg,
            kind=self.serialize_format,
            uri=uri,
        )
        try:
            # start on the top nodes
            self.run(self.top_nodes(visitor), visitor)
        except Exception as e:
            visitor.scribe.write(
                level='error',
                msg=e.__class__.__name__ + ': ' + str(e),
            )
            visitor.scribe.write(
                level='error',
                msg=format_tb(sys.exc_info()[2]),
            )

        msg = _(u'{kind} file {uri} read succesfully')
        visitor.scribe.write(
            level='info',
            msg=msg,
            kind=self.serialize_format,
            uri=uri,
        )
        visitor.scribe.write(
            level='info',
            msg=u'Harvesting real run successfully',
        )

        return visitor.scribe.html_log()

    def dry_run(self):
        visitor = DCATVisitor()
        return self.prepare_and_run(visitor)

    def real_run(self):
        visitor = RealRunVisitor()
        return self.prepare_and_run(visitor)
