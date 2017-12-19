# -*- coding: utf-8 -*-
"""Init and utils."""

import surf
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('pkan.dcatapde')



surf.ns.register(SKOS="http://www.w3.org/2004/02/skos/core#")
surf.ns.register(DCAT="http://www.w3.org/ns/dcat#")
surf.ns.register(SCHEMA="http://schema.org/")

# re-register the RDF + RDFS namespace because in new surf they are closed
# namespaces and they won't "take" the custom terms that we access on them
surf.ns.register(RDF="http://www.w3.org/1999/02/22-rdf-syntax-ns#")
surf.ns.register(RDFS="http://www.w3.org/2000/01/rdf-schema#")