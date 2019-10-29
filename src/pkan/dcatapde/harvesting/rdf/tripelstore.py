# -*- coding: utf-8 -*-
"""Tripel store access"""

from pkan.dcatapde.constants import BLAZEGRAPH_BASE
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

    def create_namespace(self, namespace):
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

        self.namespace_uris[namespace] = \
            BLAZEGRAPH_BASE + \
            '/{namespace}/sparql'.format(namespace=namespace)

        return response

    def bulk_load_from_uri(self, namespace, uri):
        params = {'uri': uri}
        blaze_uri = \
            BLAZEGRAPH_BASE + \
            '/blazegraph/namespace/{namespace}/sparql'
        blaze_uri.format(namespace=namespace)
        response = requests.post(
            blaze_uri,
            data=params,
        )
        return response


# sparql.setReturnFormat(XML)
# results = sparql.query()
# print(results)

# for result in results.bindings:
#    print(result)
#    print('%s: %s' % (result["label"].lang, result["label"].value))


tripel_store = Tripelstore()
# tripel_store.create_namespace('test3')
# tripel_store.bulk_load_from_uri('test3',
# "https://opendata.potsdam.de/api/v2/catalog/exports/ttl?rows=10&timezone=UTC&include_app_metas=false")
