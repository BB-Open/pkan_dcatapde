# -*- coding: utf-8 -*-
"""testing rdf an databases"""

from rdflib import Graph
from rdflib import Literal
from rdflib import plugin
from rdflib.store import Store
from rdflib_sqlalchemy import registerplugins


# import vkbeautify as vkb


registerplugins()


class SQLStorage(object):
    uri = Literal('sqlite://')

    def __init__(self, name):
        store = plugin.get('SQLAlchemy', Store)(identifier=name)
        self.graph = Graph(store, identifier=name)
        self.graph.open(self.uri, create=True)

    def read(self, data):
        self.graph.read(data)

# build a storage
storage = SQLStorage('test1')

# read an rdf file in the storage
# storage.graph.load('http://dbpedia.org/resource/Semantic_Web')

storage.graph.load('http://publications.europa.eu/mdr/resource/authority'
                   '/licence/skos/licences-skos.rdf')

# storage.graph.load('http://www.dcat-ap.de/def/licenses/1_0.rdf')

# print(vkb.xml(storage.graph.serialize()))

qres = storage.graph.query(
    """SELECT DISTINCT ?license ?label ?definition
       WHERE {
          ?license rdfs:isDefinedBy ?definition .
          ?license rdfs:label ?label .
       }""")


# print(vkb.xml(qres.serialize()))

storage.graph.save()
