# -*- coding: utf-8 -*-
"""Harvesting adapter."""
from DateTime.DateTime import time
from functools import partial
from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_RDF_LITERAL
from pkan.dcatapde.constants import RDF_FORMAT_JSONLD
from pkan.dcatapde.constants import RDF_FORMAT_METADATA
from pkan.dcatapde.constants import RDF_FORMAT_TURTLE
from pkan.dcatapde.constants import RDF_FORMAT_XML
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.errors import RequiredPredicateMissing
from pkan.dcatapde.harvesting.source_type.interfaces import IRDFJSONLD
from pkan.dcatapde.harvesting.source_type.interfaces import IRDFTTL
from pkan.dcatapde.harvesting.source_type.interfaces import IRDFXML
from pkan.dcatapde.harvesting.source_type.scribe import Scribe
from pkan.dcatapde.log.log import TranslatingFormatter
from pkan.dcatapde.structure.sparql import QUERY_A
from pkan.dcatapde.structure.sparql import QUERY_ATT
from pkan.dcatapde.structure.structure import IMP_REQUIRED
from pkan.dcatapde.structure.structure import StructDCATCatalog
from pkan.dcatapde.structure.structure import StructDCATDataset
from plone.api import content
from plone.api import portal
from plone.memoize import ram
from rdflib import Graph
from rdflib.namespace import FOAF
from rdflib.plugins.memory import IOMemory
from rdflib.store import Store
from zope.component import adapter
from zope.interface import implementer

import io
import logging


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
        try:
            self.harvesting_type = \
                self.harvester.harvesting_type(self.harvester)
        except TypeError:
            self.harvesting_type = None

        # fetch the preprocessor adapter
        self.data_cleaner = self.harvester.data_cleaner(self.harvester)
        self.cleaned_data = None
        # self.field_config = get_field_config(self.harvester)
        self.context = portal.get()
        if self.harvester:
            if self.harvester.base_object:
                # Todo: check why sometime to_object and sometimes not
                self.context = getattr(self.harvester.base_object,
                                       'to_object',
                                       self.harvester.base_object)

        # determine the source format serializer string for rdflib from our
        # own interface. Todo this is a bit ugly
        self.rdf_format_key = IFaceToRDFFormatKey[self.harvester.source_type]
        self.rdf_format = RDF_FORMAT_METADATA[self.rdf_format_key]
        self.serialize_format = self.rdf_format['serialize_as']
        self.def_lang = unicode(portal.get_default_language()[:2])
        self.setup_logger()

    def read_rdf_file(self, uri):
        """Load the rdf data"""
        rdfstore = Store()
        # self.session = self.harvester.rdfstore.session
        # self.harvester.rdfstore.store.load_triples(source=uri, format=format)
        graph = Graph(rdfstore)
        # graph.open(uri)
        graph.load(uri)
        return rdfstore, graph

    @property
    @ram.cache(cache_key)
    def graph(self):
        """In Memory representation of the incoming RDF graph"""
        rdfstore = IOMemory()
        _graph = Graph(rdfstore)
        _graph.load(self.harvester.url, format=self.serialize_format)
        return _graph

    def read_classes(self):
        """Read the classes of the rdf data for the vocabulary to assign
         to DX classes"""
        SPARQL = """SELECT DISCTINCT ?o WHERE {?s a ?o .}"""
        result = self.harvester.graph.query(SPARQL)
        return result

    def read_dcat_fields(self, *args, **kwargs):
        """Dummy"""
        return []

    def read_fields(self, *args, **kwargs):
        """Dummy"""
        return []

    def clean_data(self, *arg, **kwargs):
        """Dummy"""

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
        request = getattr(self.context, 'REQUEST', None)
        formatter = TranslatingFormatter(format, request=request)
        # and plug things together
        stream_handler.setFormatter(formatter)
        log.addHandler(stream_handler)
        self.log = log

    def reap_logger(self):
        """return the log output"""
        # rewind the stream
        self.log_stream.seek(0)
        # read the stream into a string
        log = self.log_stream.read()
        # get rid of the stream
        self.log_stream.close()
        # and return return the log
        return log

    def dry_run(self):
        """Dry Run: Returns Log-Information.
        """
        # Just to have the posibility to reset
        self.harvester._graph = None
        self.harvester._rdfstore = None

        self.log.info(u'starting harvestdry run')
        uri = self.harvester.url

        msg = _(
            u'Reading {kind} file {uri}',
            mapping={'kind': self.serialize_format, 'uri': uri},
        )
        self.log.info(msg)
        msg = _(
            u'{kind} file {uri} read succesfully',
            mapping={'kind': self.serialize_format, 'uri': uri},
        )
        self.log.info(msg)
        self.log.info(u'Harvesting real run successfully')

        return self.reap_logger()

    def top_nodes(self):
        """Find top nodes: Catalogs or datasets"""
        # check if we get a base object
        if self.harvester.base_object:
            self.context = content.get(UID=self.harvester.base_object)
            self.struct_class = StructDCATDataset
        else:
            self.context = portal.get()
            self.struct_class = StructDCATCatalog

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
        # Todo : handle more than one hit
        catalog = res.bindings[0]['s']

        self.crawl(self.context, catalog, self.struct_class)

    def scribe(self, level=None, msg=None, **kwargs):
        message = _(msg, mapping=kwargs)
        getattr(self.log, level)(message)

    def handle_list(self, context, res, field_name, field, obj_data, scribe):
        obj_data[field_name] = []
        for i in res.bindings:
            # If the field is a Literal we simply store it.
            if field['object'] == CT_RDF_LITERAL:
                obj_data[field_name].append(i['o'])
            # if not we have to create a sub object recursively
            else:
                sub = self.crawl(context, i['o'], field['object'])
                obj_data[field_name].append(sub)
            scribe(
                level='info',
                msg=u'{type} object {obj}: attribute {att}:= {val}',
                val=i['o'],
            )

    def handle_dict(self, context, res, field_name, field, obj_data, scribe):
        obj_data[field_name] = {}
        for i in res.bindings:
            # special handling of literals without language
            if not ('o1' in i):
                obj_data[field_name][self.def_lang] = unicode(i['o'])
                scribe(
                    level='info',
                    msg=u'{type} object {obj}: attribute {att}:= {val}',
                    val=i['o'],
                    att=field['predicate'],
                )
            else:
                obj_data[field_name][i['o1']] = unicode(i['o2'])
                scribe(
                    level='info',
                    msg=u'{type} object {obj}: attribute {att}:= {val}',
                    val=str(i['o1']) + ':' + str(i['o1']),
                    att=field['predicate'],
                )

    def properties(self, context, rdf_node, struct, obj_data, scribe):
        """At first we run over the fields and references only, to collect
        the data necessary to construct the CT instance.
        With the contained instances will be dealed if the CT instance
        is constructed"""

        # query for an attibute
        query = QUERY_ATT

        for field_name, field in struct.fields_and_referenced.items():
            # Todo : query the entity mapper
            # if struct.rdf_type in self.harvester.mapper:
            #   query = self.harvester.mapper[struct.rdf_type]
            if struct.rdf_type == FOAF.Agent and field_name == 'foaf_name':
                pass

            scribe(
                level='info',
                msg=u'{type} object {obj}: '
                    u'searching {imp} attribute {att}',
                att=field['predicate'],
                imp=field['importance'],
            )

            # Query the RDF db. Subject is the node we like
            # to construct. Predicate
            # is the attribute we like to find in the RDF
            bindings = {
                's': rdf_node,
                'p': field['predicate'],
            }
            res = self.graph.query(query, initBindings=bindings)

            # Dealing with required fields not delivered
            if len(res) == 0:
                if field['importance'] == IMP_REQUIRED:
                    scribe(
                        level='error',
                        msg=u'{type} object {obj}: required '
                            u'attribute {att} not found',
                        att=field['predicate'],
                    )
                    # Todo: Error handling
                    raise RequiredPredicateMissing()
                else:
                    scribe(
                        level='warn',
                        msg=u'{type} object {obj}: {imp} '
                            u'attribute {att} not found',
                        att=field['predicate'],
                        imp=field['importance'],
                    )
                continue

            # dealing with lis like fields
            if field['type'] == list:
                self.handle_list(
                    context,
                    res,
                    field_name,
                    field,
                    obj_data,
                    scribe,
                )

            # dealing with dict like fields aka Literals
            elif field['type'] == dict:
                self.handle_dict(
                    context,
                    res,
                    field_name,
                    field,
                    obj_data,
                    scribe,
                )
            # Iten/list collision checking. Attribute is Item in DCATapded,
            # but a list is delivered.
            elif len(res) > 1:
                scribe(
                    level='error',
                    msg=u'{type} object {obj}: '
                        u'attribute {att} to many values',
                    att=field['predicate'],
                )
                # Todo: Error handling
                break
            # Simple case of a single item
            else:
                # If the field is a Literal we simply store it.
                if field['object'] == CT_RDF_LITERAL:
                    obj_data[field_name] = res.bindings[0]['o']
                # if not we have to create a sub object recursively
                else:
                    sub = self.crawl(
                        context,
                        res.bindings[0]['o'],
                        field['object'],
                    )
                    obj_data[field_name] = sub
                scribe(
                    level='info',
                    msg=u'{type} object {obj}: attribute {att}:= {val}',
                    val=obj_data[field_name],
                    att=field['predicate'],
                )

    def contained(self, obj, rdf_node, struct, scribe):
        """At first we run over the fields and references only, to collect
        the data necessary to construct the CT instance.
        With the contained instances will be dealed if the CT instance
        is constructed"""

        # query for an attibute
        query = QUERY_ATT
        #   Handle the contained objects
        for field_name, field in struct.contained.items():
            # Todo : query the entity mapper
            # if struct.rdf_type in self.harvester.mapper:
            #                query = self.harvester.mapper[struct.rdf_type]
            scribe(
                level='info',
                msg=u'{type} object {obj}: searching contained {att}',
                att=field['predicate'],
            )

            # Query the RDF db. Subject is still the rdf_node
            # Predicate is the attribute we like to find in the RDF
            bindings = {
                's': rdf_node,
                'p': field['predicate'],
            }
            res = self.graph.query(query, initBindings=bindings)

            for i in res.bindings:
                self.crawl(obj, i['o'], field['object'])
                scribe(
                    level='info',
                    msg=u'Crawling to sub obj {obj} of type {type} '
                        u'attribute {att}',
                    att=field['predicate'],
                )

    def crawl(self, context, rdf_node, target_struct):
        """Analyse the RDF structure"""

        # Activate the struct
        struct = target_struct(self.harvester)

        # here we collect the data to generate our DX object
        obj_data = {}

        # Partial scribe with some base arguments
        scribe_kwargs = {
            'type': struct.rdf_type,
            'obj': rdf_node,
        }
        scribe = partial(self.scribe.write, **scribe_kwargs)

        try:
            # Go for the properties of the current node
            self.properties(context, rdf_node, struct, obj_data, scribe)

            # Create an instance of the node as dexterity object
            title = unicode(obj_data[struct.title_field].items()[0][1])
            obj = content.create(
                context,
                target_struct.portal_type,
                title=title,
                **obj_data)
            obj.reindexObject()
            scribe(
                level='info',
                msg=u'{type} dxobject {obj} created at {context}',
                context=context.virtual_url_path(),
            )

            self.contained(obj, rdf_node, struct, scribe)

            return obj

        except RequiredPredicateMissing:
            return None

    def real_run(self):
        """Dry Run: Returns Log-Information.
        """
        self.log.info(u'Starting real harvest run')
        uri = self.harvester.url

        msg = _(
            u'Reading {kind} file {uri} into rdflib',
            mapping={'kind': self.serialize_format, 'uri': uri},
        )
        self.log.info(msg)

        self.scribe = Scribe()

        # start on the top nodes
        self.top_nodes()

        self.log.info(u'Real harvest run successfull')

        return self.scribe.read()

    def get_preview(self):
        """Dry Run: Returns Log-Information.
        """
        return 'The preview!!!!!'
