# -*- coding: utf-8 -*-
"""Helpers for SPQRQL"""
from pkan_config.namespaces import NAMESPACES
from rdflib import Graph
from rdflib.namespace import NamespaceManager
from rdflib.plugins.sparql import prepareQuery

# Construct a namespace manager to get abbreviated URIRefs for
# known namespaces. e.g.
# dcat:Dataset instead of http://www.w3.org/ns/dcat#Dataset
namespace_manager = NamespaceManager(Graph())
for prefix, ns in NAMESPACES.items():
    namespace_manager.bind(prefix, ns)

# Give me the objects to given predicate
# "a" query
# QUERY_A_STR = u"""SELECT DISTINCT ?s
#        WHERE {
#           ?s a ?o
#        }"""
#
# QUERY_A = prepareQuery(
#     QUERY_A_STR,
#     initNs=NAMESPACES,
# )
