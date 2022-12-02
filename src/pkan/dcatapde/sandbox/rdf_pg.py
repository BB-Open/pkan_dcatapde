# -*- coding: utf-8 -*-
"""testing rdf an databases"""

import vkbeautify as vkb
from rdflib import Graph
from rdflib import Literal
from rdflib import plugin
from rdflib.store import Store
from rdflib_sqlalchemy import registerplugins
from sqlalchemy.exc import IntegrityError

registerplugins()


class SQLStorage(object):
    uri = Literal('postgresql+psycopg2://pkan:sas242@localhost:5432/pkanstore')

    def __init__(self, name):
        store = plugin.get('SQLAlchemy', Store)(identifier=name)
        self.graph = Graph(store, identifier=name)
        self.graph.open(self.uri, create=True)

    def read(self, data):
        self.graph.parse(source=data)


# build a storage
storage = SQLStorage('test1')

# read an rdf file in the storage
# storage.graph.load('http://dbpedia.org/resource/Semantic_Web')

try:
    storage.graph.parse(
        source='http://publications.europa.eu/mdr/resource/authority'
               '/licence/skos/licences-skos.rdf')
except IntegrityError:
    pass

# storage.graph.load('http://www.dcat-ap.de/def/licenses/1_0.rdf')

# print(vkb.xml(storage.graph.serialize()))

qres = storage.graph.query(
    """SELECT DISTINCT ?license ?label ?definition
       WHERE {
          ?license rdfs:isDefinedBy ?definition .
          ?license rdfs:label ?label .
       }""")

res = vkb.xml(qres.serialize())
# print(res)

# storage.graph.save()
