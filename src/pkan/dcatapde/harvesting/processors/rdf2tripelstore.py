# -*- coding: utf-8 -*-

"""Harvesting adapter."""
from SPARQLWrapper.SmartWrapper import Value
from pkan.dcatapde.constants import ADMIN_USER, ADMIN_PASS, RDF4J_BASE
from pkan.dcatapde.constants import CT_ANY
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import HARVEST_TRIPELSTORE
from pkan.dcatapde.constants import RDF_FORMAT_METADATA
from pkan.dcatapde.constants import RDF_FORMAT_TURTLE, RDF_REPO_TYPE
from pkan.dcatapde.content.rdfs_literal import literal2plone
from pkan.dcatapde.harvesting.errors import NoSourcesDefined
from pkan.dcatapde.harvesting.errors import RequiredPredicateMissing
from pkan.dcatapde.harvesting.errors import UnkownBindingType
from pkan.dcatapde.harvesting.processors.rdf_base import BaseRDFProcessor
from pkan.dcatapde.harvesting.processors.rdf_base import handle_identifiers
from pkan.dcatapde.harvesting.processors.visitors import DCATVisitor
from pkan.dcatapde.harvesting.processors.visitors import NT_RESIDUAL
from pkan.dcatapde.structure.sparql import QUERY_ALL_STR_SPARQL
from pkan.dcatapde.structure.sparql import QUERY_ATT_STR_SPARQL
from pkan.dcatapde.structure.sparql import QUERY_A_STR_SPARQL
from pkan.dcatapde.structure.sparql import QUERY_P
from pkan.dcatapde.structure.sparql import QUERY_P_STR_SPARQL
from pkan.dcatapde.structure.structure import STRUCT_BY_PORTAL_TYPE
from pkan.dcatapde.structure.structure import StructRDFSLiteral
# from pkan.blazegraph.api import tripel_store
from pyrdf4j.rdf4j import RDF4J
from rdflib.term import Literal
from rdflib.term import URIRef
from requests.auth import HTTPBasicAuth


class TripleStoreRDFProcessor(BaseRDFProcessor):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    def prepare_harvest(self, visitor):
        """Load data to be harvested into a temperary namespace
        on the tripelstore.
        Then set a rdflib grpah instance to it for reading.
        Open a target namespace for the dcat-ap.de compatible data and
        set a rdflib grpah instance to it for writing and reading.
        """
        # todo: Missing Attribute, should it be 2 or 3 letters?
        #  Should be set by harvester
        self.def_lang = 'de'

        self.tripel_db_name = self.harvester.id_in_tripel_store
        self.tripel_temp_db_name = self.tripel_db_name + '_temp'
        self.tripel_dry_run_db = self.tripel_db_name + '_dryrun'

        # todo: base in constants
        self._rdf4j = RDF4J(rdf4j_base=RDF4J_BASE)
        self.auth= HTTPBasicAuth(ADMIN_USER, ADMIN_PASS)

        if visitor.real_run:

            # todo: Type in constants, is this correct type
            self._rdf4j.create_repository(self.tripel_temp_db_name, repo_type=RDF_REPO_TYPE, overwrite=False, accept_existing=True, auth=self.auth)
            self._rdf4j.create_repository(self.tripel_db_name, repo_type=RDF_REPO_TYPE, overwrite=False, accept_existing=True, auth=self.auth)

            # self._graph, _response = tripel_store.graph_from_uri(
            #     tripel_temp_db_name,
            #     self.harvester.url,
            #     self.harvester.mime_type,
            #     clear_namespace=True,
            # )
            # tripel_store.empty_namespace(tripel_db_name)
            # self._target_graph = tripel_store.create_namespace(tripel_db_name)
            self.query_db = self.tripel_temp_db_name
        else:
            # todo: dry run should know nothing about store,
            #  but if we use IOMemory store all Queries and results are
            #  different
            # todo: Work around: We update '_temp' and use it,
            #  but do not write to clean store
            self._rdf4j.create_repository(self.tripel_dry_run_db, repo_type=RDF_REPO_TYPE, overwrite=True, auth=self.auth)
            self.query_db = self.tripel_dry_run_db

        msg = u'Working on {url}'.format(url=self.harvester.url)
        visitor.scribe.write(
            level='info',
            msg=msg,
        )

        self._rdf4j.bulk_load_from_uri(self.query_db, self.harvester.url, self.harvester.mime_type, auth=self.auth, clear_repository=True)
        if visitor.real_run:
            self._rdf4j.empty_repository(self.tripel_db_name, auth=self.auth)

    @property
    def rdf4j(self):
        """Interface to incoming RDF graph"""
        if not self._rdf4j:
            self.prepare_harvest()
        return self._rdf4j

    def query(self, query, bindings):
        query_params = {}
        for key, binding in bindings.items():
            if isinstance(binding, Value):
                if binding.type == 'uri':
                    query_params[key] = '<' + binding.value + '>'
                elif binding.type == 'literal':
                    query_params[key] = '"' + binding.value + '"'
                else:
                    raise UnkownBindingType
            elif isinstance(binding, URIRef):
                query_params[key] = '<' + str(binding) + '>'
            else:
                if str(binding)[0] not in ['"', '<']:
                    if key in ['s', 'p']:
                        query_params[key] = '<' + str(binding) + '>'
                    else:
                        query_params[key] = '"' + str(binding) + '"'
                else:
                    query_params[key] = str(binding)

        prepared_query = query.format(**query_params)
        response = self.rdf4j.query_repository(self.query_db, prepared_query, auth=self.auth)
        res = response['results']['bindings']
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
        for i in res:
            rdf_obj = i['o']
            # special handling of literals without language
            if 'xml:lang' not in rdf_obj:
                obj_data[field_name][self.def_lang] = rdf_obj['value']
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
                    val=str(rdf_obj['value']) + u':' + str(rdf_obj['xml:lang']),
                    att=predicate,
                    obj=kwargs['rdf_node'],
                    type=kwargs['struct'].rdf_type,
                )

            visitor.end_node(predicate, obj_class, **kwargs)

    def insert(self, s, p, o):
        s_out = '<' + s['value'] + '>'
        if isinstance(p, str):
            p_out = '<' + p + '>'
        elif p['type'] == 'uri':
            p_out = '<' + p['value'] + '>'
        else:
            p_out = '"' + self.escape_literal(p['value']) + '"'
        if o['type'] == 'uri':
            o_out = '<' + o['value'] + '>'
        else:
            o_out = '"' + self.escape_literal(o['value']) + '"'
            if 'xml:lang' in o:
                o_out += '@' + o['xml:lang']
        INSERT = """{s} {p} {o} ."""
        insert = INSERT.format(
            s=s_out,
            p=p_out,
            o=o_out,
        )
        return self.rdf4j.add_data_to_repo(self.tripel_db_name, insert.encode('utf-8'), 'text/turtle', auth=self.auth)
        # self.target_graph.sparql.setQuery(query=insert)
        # res = self.target_graph.sparql.query()
        # return res

    def construct(self, rdf_node, data, struct=None):
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

        if rdf_node['type'] == 'literal':
            return
        prepared_query = QUERY.format(
            rdf_node='<' + rdf_node['value'] + '>',
            filter=filter,
        )

        results = self.rdf4j.query_repository(self.query_db, prepared_query, auth=self.auth)['results']['bindings']

        # do not add invalid attributes, which can be find by query, but set None in data
        unwanted_fields = []
        for field in data:
            if data[field] is None:
                if field in struct.fields_and_referenced:
                    unwanted_fields.append(struct.fields_and_referenced[field]['predicate'].toPython())

        for res in results:
            if res['p']['value'] in unwanted_fields:
                continue
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
        if visitor.real_run:

            self.construct(rdf_node, obj_data, struct)

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
        return obj_data

    def crawl(
        self,
        visitor,
        target_struct=None,
        context=None,
        rdf_node=None,
    ):
        # todo: is context always non in this method?
        context = None

        # Return if we have hit a Blank node
        if rdf_node['type'] == 'bnode':
            return None

        # Activate the struct
        struct = target_struct(self.harvester)

        # here we collect the data to generate our DX object
        obj_data = {}

        # set the original URI as rdf_about field:

        obj_data['rdf_about'] = rdf_node['value']

        # Go for the DCAT-AP.de properties of the current node
        try:
            self.properties(
                visitor,
                context=context,
                rdf_node=rdf_node,
                struct=struct,
                obj_data=obj_data,
            )
        except RequiredPredicateMissing:
            # if a property is missing, we return None. Object is not available
            return None
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
            title = self.get_title(struct, obj_data, visitor)

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
                msg=u'{type} object {obj} cannot be created.',
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

    def top_nodes(self, visitor):
        """Find top nodes: Catalogs or datasets"""

        top_node_class = self.harvester.top_node

        if top_node_class == CT_ANY:
            res = self.query_all()
            for top_node in res:
                yield top_node['s']

        else:
            struct_class = STRUCT_BY_PORTAL_TYPE[top_node_class]

            res = self.query_a(struct_class.rdf_type)

            for top_node in res:
                yield top_node['s']


class MultiUrlTripleStoreRDFProcessor(TripleStoreRDFProcessor):

    def prepare_harvest(self, visitor):
        """Load data to be harvested into a temperary namespace
                on the tripelstore.
                Then set a rdflib grpah instance to it for reading.
                Open a target namespace for the dcat-ap.de compatible data and
                set a rdflib grpah instance to it for writing and reading.
                """
        # todo: Missing Attribute, should it be 2 or 3 letters?
        #   Should be set by harvester
        if not self.harvester.catalog_urls:
            raise NoSourcesDefined('You did not define any sources')

        self.def_lang = 'de'

        tripel_db_name = self.harvester.id_in_tripel_store
        tripel_temp_db_name = tripel_db_name + '_temp'
        tripel_dry_run_db = tripel_db_name + '_dryrun'

        sources = self.harvester.catalog_urls

        self.tripel_db_name = self.harvester.id_in_tripel_store
        self.tripel_temp_db_name = self.tripel_db_name + '_temp'
        self.tripel_dry_run_db = self.tripel_db_name + '_dryrun'

        # todo: base in constants
        self._rdf4j = RDF4J(rdf4j_base=RDF4J_BASE)
        self.auth = HTTPBasicAuth(ADMIN_USER, ADMIN_PASS)

        if visitor.real_run:

            # todo: Type in constants, is this correct type
            self._rdf4j.create_repository(self.tripel_temp_db_name, repo_type=RDF_REPO_TYPE, overwrite=True,
                                          auth=self.auth)
            self._rdf4j.create_repository(self.tripel_db_name, repo_type=RDF_REPO_TYPE, accept_existing=True,
                                          auth=self.auth)

            # self._graph, _response = tripel_store.graph_from_uri(
            #     tripel_temp_db_name,
            #     self.harvester.url,
            #     self.harvester.mime_type,
            #     clear_namespace=True,
            # )
            # tripel_store.empty_namespace(tripel_db_name)
            # self._target_graph = tripel_store.create_namespace(tripel_db_name)
            self.query_db = self.tripel_temp_db_name
        else:
            # todo: dry run should know nothing about store,
            #  but if we use IOMemory store all Queries and results are
            #  different
            # todo: Work around: We update '_temp' and use it,
            #  but do not write to clean store
            self._rdf4j.create_repository(self.tripel_dry_run_db, repo_type=RDF_REPO_TYPE, overwrite=True,
                                          auth=self.auth)
            self.query_db = self.tripel_dry_run_db

        # append for all the others
        for source in sources:
            msg = u'Working on {url}'.format(url=source)
            visitor.scribe.write(
                level='info',
                msg=msg,
            )
            self._rdf4j.bulk_load_from_uri(self.query_db, source, self.harvester.mime_type, auth=self.auth)


def main():
    from addict import Dict

    harvester = Dict()

    harvester.url = 'https://opendata.potsdam.de/api/v2/catalog/exports/ttl'
    harvester.base_object = None
    harvester.source_type = RDF_FORMAT_TURTLE
    harvester.serialize_format = RDF_FORMAT_METADATA[harvester.source_type]['serialize_as']  # noqa: E501
    harvester.mime_type = RDF_FORMAT_METADATA[harvester.source_type]['mime_type']  # noqa: E501
    harvester.target = HARVEST_TRIPELSTORE

    # todo: should be one attribute, cause we just have one namespace name
    harvester.id_in_tripel_store = 'test2NS'
    harvester.target_namespace = 'test2NS'

    harvester.top_node = CT_DCAT_CATALOG

    rdf_import = TripleStoreRDFProcessor(harvester)
    visitor = DCATVisitor()
    visitor.real_run = False
    rdf_import.prepare_and_run(visitor)


if __name__ == '__main__':
    main()
