# -*- coding: utf-8 -*-
"""testing rdf an databases"""

from rdflib import Graph
from rdflib import Literal
from rdflib import plugin
from rdflib.store import Store
from rdflib_sqlalchemy import registerplugins

import surf


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


store = surf.Store(
    reader='rdflib',
    writer='rdflib',
    rdflib_store='IOMemory',
)

session = surf.Session(store)

# print("Load RDF data")
store.load_triples(source='http://www.dcat-ap.de/def/licenses/1_0.rdf')

Person = session.get_class(surf.ns.FOAF['Person'])

all_persons = Person.all()
