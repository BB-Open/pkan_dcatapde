# -*- coding: utf-8 -*-
"""Tripel store access"""

from pkan.dcatapde.constants import BLAZEGRAPH_BASE
from pkan.dcatapde.harvesting.errors import HarvestURINotReachable
from pkan.dcatapde.harvesting.errors import TripelStoreBulkLoadError
from pkan.dcatapde.harvesting.errors import TripelStoreCreateNamespaceError
from SPARQLWrapper import SPARQLWrapper2

import requests


class SPARQL(object):
    """
    API to the SPARQL Endpoint of a namespace
    """

    def __init__(self, uri):
        self.sparql = SPARQLWrapper2(uri)

    def exists(self, URI):
        self.sparql.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?s
            WHERE { ?s ?p ?o }
                    """)
        results = self.sparql.query()
        if results:
            return True

    def insert(self, tripel):
        queryString = """INSERT DATA
           {{ GRAPH <http://example.com/> {{ {s} {p} {o} }} }}"""

        self.sparql.setQuery(
            queryString.format(s=tripel.s, o=tripel.o, p=tripel.p))
        self.sparql.method = 'POST'
        self.sparql.query()


class Tripelstore(object):
    """
    API to the tripelstore
    """

    def __init__(self):

        self.namespace_uris = {}

    def sparql_for_namespace(self, namespace):
        return SPARQL(self.namespace_uris[namespace])

    def rest_create_namespace(self, namespace):
        """
        Creates a namespace in the tripelstore and registers
        a namespace sparqlwrapper for it
        :param namespace: Then namespace to be created
        :return:
        """
        params = """
        com.bigdata.rdf.sail.namespace={namespace}
        com.bigdata.rdf.sail.truthMaintenance=false
        com.bigdata.namespace.{namespace}.spo.com.bigdata.btree.BTree.branchingFactor=1024
        com.bigdata.rdf.store.AbstractTripleStore.textIndex=true
        com.bigdata.rdf.store.AbstractTripleStore.justify=false
        com.bigdata.rdf.store.AbstractTripleStore.statementIdentifiers=false
        com.bigdata.rdf.store.AbstractTripleStore.axiomsClass=com.bigdata.rdf.axioms.NoAxioms
        com.bigdata.rdf.store.AbstractTripleStore.quads=false
        com.bigdata.namespace.{namespace}.lex.com.bigdata.btree.BTree.branchingFactor=400
        com.bigdata.rdf.store.AbstractTripleStore.geoSpatial=false
        com.bigdata.journal.Journal.groupCommit=false
        com.bigdata.rdf.sail.isolatableIndices=false
        """.format(namespace=namespace)
        headers = {'content-type': 'text/plain'}
        response = requests.post(
            BLAZEGRAPH_BASE + '/blazegraph/namespace',
            data=params,
            headers=headers,
        )
        blaze_uri = BLAZEGRAPH_BASE + \
            '/blazegraph/namespace/{namespace}/sparql'
        blaze_uri_with_namespace = blaze_uri.format(namespace=namespace)
        self.namespace_uris[namespace] = blaze_uri_with_namespace

        return response

    def rest_bulk_load_from_uri(self, namespace, uri, content_type):
        """
        Load the tripel_data from the harvest uri
        and push it into the tripelstore
        :param namespace:
        :param uri:
        :param content_type:
        :return:
        """
        # Load the tripel_data from the harvest uri
        response = requests.get(uri)
        if response.status_code != 200:
            raise HarvestURINotReachable(response.content)
        tripel_data = response.content

        # push it into the tripelstore
        blaze_uri = \
            BLAZEGRAPH_BASE + \
            '/blazegraph/namespace/{namespace}/sparql'
        blaze_uri_with_namespace = blaze_uri.format(namespace=namespace)
        headers = {'Content-Type': content_type}
        response = requests.post(
            blaze_uri_with_namespace,
            data=tripel_data,
            headers=headers,
        )
        return response

    def graph_from_uri(self, namespace, uri, content_type):
        self.create_namespace(namespace)
        response = self.rest_bulk_load_from_uri(namespace, uri, content_type)
        if response.status_code == 200:
            return self.sparql_for_namespace(namespace)
        else:
            raise TripelStoreBulkLoadError(response.content)

    def create_namespace(self, namespace):
        response = self.rest_create_namespace(namespace)
        if response.status_code in [200, 201, 409]:
            return self.sparql_for_namespace(namespace)
        else:
            msg = str(response.status_code) + ': ' + response.content
            raise TripelStoreCreateNamespaceError(msg)


# ToDo make to utility
tripel_store = Tripelstore()
