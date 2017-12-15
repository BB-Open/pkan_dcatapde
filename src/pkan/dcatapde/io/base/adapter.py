

import surf

store = surf.Store(reader = "rdflib",
                   writer = "rdflib",
                   rdflib_store = "IOMemory")

session = surf.Session(store)

print "Load RDF data"
store.load_triples(source = "http://datosabiertos.laspalmasgc.es/dcat")

#store.load_triples(source = "file:///home/volker/Downloads/validation/RDF/dcat_ap_de-RefImp_RDF_MIN_V1.0.rdf")


Person = session.get_class(surf.ns.FOAF["Person"])

all_persons = Person.all()

print "Found %d persons in Tim Berners-Lee's FOAF document" % (len(all_persons))
for person in all_persons:
    print person.foaf_name.first