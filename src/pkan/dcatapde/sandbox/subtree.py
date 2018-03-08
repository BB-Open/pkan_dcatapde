# -*- coding: utf-8 -*-
from pkan.dcatapde.structure.sparql import DCAT
from pkan.dcatapde.structure.sparql import QUERY_A
from rdflib import Graph
from rdflib import URIRef
from rdflib.plugins.memory import IOMemory


MAX_DEPTH = 5


def p_to_string(p):
    p = str(p)
    p.strip('/')  # if url ends with /
    p_splitted = p.split('/')
    # todo: here better short names
    return p_splitted[-1]


def get_nodes_for_ref(ref, depth=0):
    # print('Ref: %s' % ref)
    # print('-' * 80)
    res = {}
    next_depth = depth + 1
    for s, p, o in graph.triples((ref, None, None)):
        p = p_to_string(p)
        # print('S: %s, P: %s, O: %s' % (s, p,o))
        if s not in res:
            res[s] = {}
        if isinstance(o, URIRef) and depth <= MAX_DEPTH:
            res[s][p] = get_nodes_for_ref(o, depth=next_depth)
        elif isinstance(o, URIRef):
            # print('Subelements ignored by Max Depth')
            res[s][p] = o
        else:
            res[s][p] = o
    return res

url = 'https://opendata.potsdam.de/api/v2/catalog/exports/' \
      'rdf?rows=10&timezone=UTC&include_app_metas=false'

rdfstore = IOMemory()
graph = Graph(rdfstore)
graph.load(url)

res_dict = {}

qres = graph.query(QUERY_A, initBindings={'o': DCAT.Catalog})

for result in qres.bindings:
    ref = result.items()[0][1]
    res_dict.update(get_nodes_for_ref(ref))

# print(res_dict)
