# -*- coding: utf-8 -*-
"""Helpers for SPQRQL"""

from .namespaces import INIT_NS
from rdflib import Graph
from rdflib.namespace import NamespaceManager
from rdflib.plugins.sparql import prepareQuery


# Construct a namespace manager to get abbreviated URIRefs for
# known namespaces. e.g.
# dcat:Dataset instead of http://www.w3.org/ns/dcat#Dataset
namespace_manager = NamespaceManager(Graph())
for prefix, ns in INIT_NS.items():
    namespace_manager.bind(prefix, ns)

# Give me the object to a given subject and predicate.
# E.g. give me the dct:publisher to a dcat:Catalog
QUERY_ATT_STR = u"""SELECT DISTINCT ?o
       WHERE {
          ?s ?p ?o
       }"""

QUERY_ATT = prepareQuery(
    QUERY_ATT_STR,
    initNs=INIT_NS,
)

# Give me the objects to given predicate
# "a" query
QUERY_A_STR = u"""SELECT DISTINCT ?s
       WHERE {
          ?s a ?o
       }"""

QUERY_A = prepareQuery(
    QUERY_A_STR,
    initNs=INIT_NS,
)

# Give me all predicates of the current subject
QUERY_P_STR = u"""SELECT DISTINCT ?p ?o
       WHERE {
          ?s ?p ?o
       }"""

QUERY_P = prepareQuery(
    QUERY_P_STR,
    initNs=INIT_NS,
)
