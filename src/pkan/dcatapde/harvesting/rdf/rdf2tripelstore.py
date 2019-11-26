# -*- coding: utf-8 -*-
"""Harvesting adapter."""
from DateTime.DateTime import time
from pkan.blazegraph.api import tripel_store
from pkan.dcatapde.constants import RDF_FORMAT_JSONLD
from pkan.dcatapde.constants import RDF_FORMAT_TURTLE
from pkan.dcatapde.constants import RDF_FORMAT_XML
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.content.rdfs_literal import literal2plone
from pkan.dcatapde.harvesting.errors import RequiredPredicateMissing
from pkan.dcatapde.harvesting.errors import UnkownBindingType
from pkan.dcatapde.harvesting.rdf.interfaces import IRDFJSONLD
from pkan.dcatapde.harvesting.rdf.interfaces import IRDFTTL
from pkan.dcatapde.harvesting.rdf.interfaces import IRDFXML
from pkan.dcatapde.harvesting.rdf.rdf2plone import RDFProcessor
from pkan.dcatapde.harvesting.rdf.visitors import NT_RESIDUAL
from pkan.dcatapde.structure.sparql import QUERY_A_STR_SPARQL
from pkan.dcatapde.structure.sparql import QUERY_ALL_STR_SPARQL
from pkan.dcatapde.structure.sparql import QUERY_ATT_STR_SPARQL
from pkan.dcatapde.structure.sparql import QUERY_P
from pkan.dcatapde.structure.sparql import QUERY_P_STR_SPARQL
from pkan.dcatapde.structure.structure import StructRDFSLiteral
from rdflib.term import Literal
from rdflib.term import URIRef
from SPARQLWrapper.SmartWrapper import Value
from urllib import parse
from zope.component import adapter
from zope.interface import implementer


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


@adapter(IHarvester)
@implementer(IRDFTTL)
@implementer(IRDFJSONLD)
@implementer(IRDFXML)
class RDFProcessorTS(RDFProcessor):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    def __init__(self, harvester, raise_exceptions=True):
        super(RDFProcessorTS, self).__init__(harvester, raise_exceptions)
        self.tripel_tempdb = None    # Temporary tripel store
        self.tripeldb = None         # Tripestore for dcapt-ap.de data
        self._target_graph = None        # Target graph instance

    def prepare_harvest(self):
        """Load data to be harvested into a temperary namespace on the tripelstore.
        Then set a rdflib grpah instance to it for reading.
        Open a target namespace for the dcat-ap.de compatible data and
        set a rdflib grpah instance to it for writing and reading.
        """

        tripel_db_name = self.harvester.id_in_tripel_store()
        tripel_temp_db_name = tripel_db_name + '_temp'

        self._graph = tripel_store.graph_from_uri(
            tripel_temp_db_name,
            self.harvester.url,
            self.mime_type,
        )
        self._target_graph = tripel_store.create_namespace(tripel_db_name)

    @property
    def graph(self):
        """Interface to incoming RDF graph"""
        if not self._graph:
            self.prepare_harvest()
        return self._graph

    @property
    def target_graph(self):
        """Interface to the target graph in the tripel store"""
        return self._target_graph

    def query(self, query, bindings):
        for key, binding in bindings.items():
            if isinstance(binding, Value):
                if binding.type == 'uri':
                    bindings[key] = '<' + binding.value + '>'
                elif binding.type == 'literal':
                    bindings[key] = '"' + binding.value + '"'
                else:
                    raise UnkownBindingType

            elif isinstance(binding, URIRef):
                bindings[key] = '<' + binding + '>'
            else:
                if binding[0] not in ['"', '<']:
                    if key in ['s', 'p']:
                        bindings[key] = '<' + binding + '>'
                    else:
                        bindings[key] = '"' + binding + '"'

        prepared_query = query.format(**bindings)
        self.graph.sparql.setQuery(prepared_query)
        res = self.graph.sparql.query()
        return res

    def query_all(self):
        """Query the RDF db for all objects
        """

        query = QUERY_ALL_STR_SPARQL
        bindings = {
        }
        res = self.query(query, bindings)
        return res

    def query_a(self, o):
        """Query the RDF db for a given object type
        """

        query = QUERY_A_STR_SPARQL
        bindings = {
            'o': o,
        }
        return self.query(query, bindings)

    def query_attribute(self, s, p):
        """Query the RDF db. Subject is the node we are on
        Predicate is the attribute we like to find in the RDF
        """

        query = QUERY_ATT_STR_SPARQL
        bindings = {
            's': s,
            'p': p,
        }
        return self.query(query, bindings)

    def query_predicates(self, s):
        """Query the RDF db. Subject is the node we are on
        """

        query = QUERY_P_STR_SPARQL
        bindings = {
            's': s,
        }
        return self.query(query, bindings)

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

    def checkURI(self, uri, field_name=None):
        """
        To be implemented
        :param uri:
        :param field_name:
        :return:
        """
        return

    def handle_dict(self, visitor, res, **kwargs):
        obj_data = kwargs['obj_data']
        field_name = kwargs['field_name']
        field = kwargs['field']
        predicate = field['predicate']
        obj_class = field['object']

        obj_data[field_name] = {}
        for i in res.bindings:
            rdf_obj = i['o']
            # special handling of literals without language
            if not rdf_obj.lang:
                obj_data[field_name][self.def_lang] = rdf_obj.value
                visitor.scribe.write(
                    level='info',
                    msg=u'{type} object {obj}: attribute {att}:= {val}',
                    val=rdf_obj,
                    att=field['predicate'],
                    obj=kwargs['rdf_node'],
                    type=kwargs['struct'].rdf_type,
                )
            else:
                lit_dict = self.literal_handler.literal2dict_ts(rdf_obj)
                obj_data[field_name].update(lit_dict)
                visitor.scribe.write(
                    level='info',
                    msg=u'{type} object {obj}: attribute {att}:= {val}',
                    val=str(rdf_obj.value) + u':' +
                        str(rdf_obj.lang),
                    att=predicate,
                    obj=kwargs['rdf_node'],
                    type=kwargs['struct'].rdf_type,
                )

            visitor.end_node(predicate, obj_class, **kwargs)

    def insert(self, s, p, o):
        # Todo melt with self.query
        if p.type == 'uri':
            p_out = '<' + p.value + '>'
        else:
            p_out = '"' + p.value + '"'
        if o.type == 'uri':
            o_out = '<' + o.value + '>'
        else:
            o_out = '"' + o.value + '"'
        INSERT = """INSERT DATA {{ <{s}> {p} {o} . }}"""
        insert = INSERT.format(
            s=s,
            p=p_out,
            o=o_out,
        )
        self.target_graph.sparql.setQuery(query=insert)
        res = self.target_graph.sparql.query()
        return res

    def construct(self, rdf_node, struct=None):
        """
        Construct a subgraph containing all the 'properties' of the rdf_node
        entity WITHOUT the 'contained' entities.

        :param rdf_node:
        :param struct:
        :return:
        """

        FILTER = """
        FILTER NOT EXISTS {{
               VALUES ?clazz {{ {classes_comb} }}
               ?o rdf:type ?clazz.
        }}"""

        QUERY = """
        select ?s ?p ?o
        where {{ {rdf_node} ?p ?o .
                {filter}
        }}
        """
        if struct:
            classes_list = ['<' + i['target'] + '>' for i in struct.contained.values()]  # noqa: E501
            classes_comb = ' '.join(classes_list)
            filter = FILTER.format(classes_comb=classes_comb)
        else:
            filter = ''

        prepared_query = QUERY.format(
            rdf_node='<' + rdf_node.value + '>',
            filter=filter,
        )

        self.graph.sparql.setQuery(prepared_query)
        results = self.graph.sparql.query()

        for res in results.bindings:
            self.insert(
                s=rdf_node,
                p=res['p'],
                o=res['o'],
            )

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

        self.construct(rdf_node, struct)

        # Handle identifier fields
        identifier_fields = handle_identifiers(rdf_node)
        obj_data.update(identifier_fields)

        visitor.scribe.write(
            level='info',
            msg=u'{type} node {obj} created at {context}',
            context=rdf_node,
            obj=rdf_node,
            type=struct.rdf_type,
        )
        return None

    def crawl(
        self,
        visitor,
        target_struct=None,
        context=None,
        rdf_node=None,
    ):
        # Return if we have hit a Blank node
        if isinstance(rdf_node, Value):
            if rdf_node.type == 'bnode':
                return None

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

            # Hack for convention 31: Handle dct_format as literal
            if struct.literal_field is not None:
                if isinstance(title, Literal):
                    lit2dict = self.literal_handler.literal2dict(title)
                    obj_data[struct.literal_field] = lit2dict
                else:
                    obj_data[struct.literal_field] = title

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
