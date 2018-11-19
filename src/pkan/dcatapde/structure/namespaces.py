# -*- coding: utf-8 -*-

from rdflib.namespace import DC
from rdflib.namespace import DCTERMS
from rdflib.namespace import FOAF
from rdflib.namespace import Namespace
from rdflib.namespace import RDF
from rdflib.namespace import RDFS
from rdflib.namespace import SKOS


DCT = DCTERMS
DCAT = Namespace('http://www.w3.org/ns/dcat#')
DCATDE = Namespace('http://dcat-ap.de/def/dcatde/1_0')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')
ADMS = Namespace('http://www.w3.org/ns/adms#')

# List of namespaces for SPARQL Queries.
# Todo: would be good if this list came from the plone config
INIT_NS = {
    'dct': DCTERMS,
    'foaf': FOAF,
    'skos': SKOS,
    'dcat': DCAT,
    'dcatde': DCATDE,
    'rdf': RDF,
    'rdfs': RDFS,
    'vcard': VCARD,
    'dc': DC,
    'adms': ADMS,
}
