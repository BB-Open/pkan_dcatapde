# -*- coding: utf-8 -*-
"""Harvesting adapter."""
from DateTime.DateTime import time
from pkan.dcatapde import _
from pkan.dcatapde.content.rdfs_literal import literal2plone
from pkan.dcatapde.harvesting.errors import RequiredPredicateMissing
from pkan.dcatapde.harvesting.processors.visitors import Node
from pkan.dcatapde.harvesting.processors.visitors import NS_ERROR
from pkan.dcatapde.harvesting.processors.visitors import NS_WARNING
from pkan.dcatapde.structure.structure import IMP_REQUIRED
from pkan.dcatapde.structure.structure import STRUCT_BY_NS_CLASS
from pkan.dcatapde.structure.structure import StructRDFSLiteral
from rdflib.term import URIRef
from SPARQLWrapper.SmartWrapper import Value
from traceback import format_tb
from urllib import parse

import rdflib
import sys


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


def handle_identifiers(obj):
    """
    Handle Konv 24/25/26/27
    Deal with duplicates and push trough Id information
    """

    params = {}

    # Special case of dct_identifier. If dct:identifier is set conserve it.
    dct_identifier = str(getattr(obj, 'dct_identifier', None))
    if isinstance(obj, URIRef):
        subject = str(obj)
    else:
        try:
            subject = str(getattr(obj, 'subject'))
        except AttributeError:
            # This is the case for Literal
            subject = None

    # if no dct:Identifier is set
    if dct_identifier is None:
        # set it to the subject
        params['dct_identifier'] = subject
    else:
        # check if dct:Identifier is really an URI
        if parse.urlparse(dct_identifier).scheme != '':
            params['dct_identifier'] = dct_identifier
        else:
            params['dct_identifier'] = subject

            # Special case of adms_identifier. If adms:identifier is set
    # conserve it.
    adms_identifier = str(getattr(obj, 'adms_identifier', None))
    if adms_identifier is not None:
        # check if adms:dientifier is really an URI
        if parse.urlparse(adms_identifier).scheme != '':
            params['adms_identifier'] = adms_identifier
        else:
            params['adms_identifier'] = None
    else:
        params['adms_identifier'] = None

    return params


class BaseRDFProcessor(object):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    raise_exceptions = True

    struct_class = None             # Todo: Is this useful
    harvesting_context = None       # Todo: Is this useful

    def __init__(self, harvester):
        self.harvester = harvester
        self.setup_logger()

    def prepare_harvest(self, visitor):
        pass

    def setup_logger(self):
        """Log to a io.stream that can later be embedded in the view output"""
        pass

    def top_nodes(self, visitor):
        """Find top nodes: Catalogs or datasets"""
        pass

    def query_all(self):
        """Query the RDF db for all objects
        """
        pass

    def query_a(self, o):
        """Query the RDF db for a given object type
        """
        pass

    def query_attribute(self, s, p):
        """Query the RDF db. Subject is the node we are on
        Predicate is the attribute we like to find in the RDF
        """
        pass

    def query_predicates(self, s):
        """Query the RDF db. Subject is the node we are on
        """
        pass


    def handle_list(self, visitor, res, **kwargs):
        pass

    def handle_dict(self, visitor, res, **kwargs):
        pass

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

        params = kwargs.copy()


        res = self.query_attribute(kwargs['rdf_node'], field['predicate'])

        # Dealing with required fields not delivered
        if len(res.bindings) == 0:
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
                raise RequiredPredicateMissing
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
            elif len(res.bindings) > 1:
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
                        #todo: check if rdf_about ist the correct field
                        obj_data[field_name] = sub['rdf_about']
                    else:
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
                            raise RequiredPredicateMissing
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
        pass

    def residual(self, visitor, predicate_object, **kwargs):
        """Handle on residual"""
        pass

    def contained(self, visitor, **kwargs):
        """At first we run over the fields and references only, to collect
        the data necessary to construct the CT instance.
        With the contained instances will be dealed if the CT instance
        is constructed"""

        struct = kwargs['struct']
        rdf_node = kwargs['rdf_node']
        context = kwargs['obj']

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

            res = self.query_attribute(rdf_node, predicate)

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

                # todo: why problems in test?
                try:
                    self.insert(rdf_node, field['predicate'], rdf_obj)
                except AttributeError:
                    pass

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
                    title = str(list(all_titles.items())[0][1])
                elif isinstance(all_titles, list):
                    title = str(all_titles[0])
                else:
                    title = all_titles
            except KeyError:
                continue
        if not title:
            raise RequiredPredicateMissing
        return title

    def checkURI(self, uri, field_name=None):
        pass


    def create_entity(
        self,
        visitor,
        struct,
        context,
        rdf_node,
        obj_data,
        title,
    ):
        pass


    def crawl(
        self,
        visitor,
        target_struct=None,
        context=None,
        rdf_node=None,
    ):
        pass


    def crawl_dx(
        self,
        visitor,
        target_struct=None,
        context=None,
        rdf_node=None,
    ):
        pass

    def parse_dcat_data(self):
        """Parsing the data in respect to the dcat ap.de diagram
        """
        pass

    def parse_input_data(self):
        """Parsing the data with focus on the input data
        """
        pass

    def get_preview(self, query, bindings={}):
        """
        Preview for sparqle_query
        """
        pass


    def remove_objects(self):
        pass



    def run(self, top_nodes, visitor):
        """crawl the top nodes"""
        for top_node in top_nodes:
            if isinstance(top_node, Value):
                top_node = top_node

            msg = _(u'Reading {top_node}')
            visitor.scribe.write(
                level='info',
                msg=msg,
                kind=self.harvester.serialize_format,
                top_node=top_node,
            )
            if self.struct_class:
                struct = self.struct_class(self.harvester)
                struct_class = self.struct_class
            else:
                node_type = self.query_attribute(
                    top_node,
                    '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>',
                )
                node_type_value = node_type.bindings[0]['o'].value
                node_type_class = rdflib.term.URIRef(node_type_value)
                struct_class = STRUCT_BY_NS_CLASS[node_type_class]
                struct = struct_class(self.harvester)

            args = {
                'structure': struct,
            }
            node = Node(**args)
            visitor.push_node(node)

            self.crawl(
                visitor,
                context=self.harvesting_context,
                rdf_node=top_node,
                target_struct=struct_class,
            )
            msg = _(u'Finished reading of {top_node}')
            visitor.scribe.write(
                level='info',
                msg=msg,
                kind=self.harvester.serialize_format,
                top_node=top_node,
            )

    def prepare_and_run(self, visitor):
        """Dry Run: Returns Log-Information.
        """

        # Connect to the data to be harvested
        self.prepare_harvest(visitor)

        if visitor.real_run:
            msg = u'starting harvest real run'
        else:
            msg = u'starting harvest dry run'
        visitor.scribe.write(
            level='info',
            msg=msg,
        )

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
            kind=self.harvester.serialize_format,
            uri=uri,
        )
        try:
            # start on the top nodes
            self.run(self.top_nodes(visitor), visitor)

        except RequiredPredicateMissing:
            return visitor.scribe.html_log()
        except Exception as e:
            visitor.scribe.write(
                level='error',
                msg='{error}',
                error=e.__class__.__name__ + ': ' + str(e),
            )
            visitor.scribe.write(
                level='error',
                msg='{error}',
                error=format_tb(sys.exc_info()[2]),
            )
            if self.raise_exceptions:
                raise e

        msg = _(u'{kind} file {uri} read succesfully')
        visitor.scribe.write(
            level='info',
            msg=msg,
            kind=self.harvester.serialize_format,
            uri=uri,
        )

        if visitor.real_run:
            msg = u'Finished harvest real run'
        else:
            msg = u'Finished harvest dry run'
        visitor.scribe.write(
            level='info',
            msg=msg,
        )

        return visitor.scribe.html_log()


