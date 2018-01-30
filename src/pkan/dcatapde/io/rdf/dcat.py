# -*- coding: utf-8 -*-
"""DCAT 2 RDF."""

from pkan.dcatapde.content.dcat_catalog import IDCATCatalog
from pkan.dcatapde.content.foaf_agent import IFOAFagent
from pkan.dcatapde.io.rdf.dexterity import Dexterity2Surf
from pkan.dcatapde.io.rdf.interfaces import ISurfSession
from zope.component import adapter

import surf


class FOAF2Surf(Dexterity2Surf):
    """Dexterity implementation of the Object2Surf."""

    adapter(IFOAFagent, ISurfSession)

    _whitelist = ['name']

    # Stores the namespace for this resource
    _namespace = surf.ns.FOAF
    _prefix = 'foaf'


class Catalog2Surf(Dexterity2Surf):
    """Dexterity implementation of the Object2Surf."""

    adapter(IDCATCatalog, ISurfSession)

    _whitelist = [
        'title',
        'description',
        'publisher',
        'add_title',
        'add_description',
    ]

    # Stores the namespace for this resource
    _namespace = surf.ns.DCAT
    _prefix = 'dcat'
