# -*- coding: utf-8 -*-
"""DCAT 2 RDF."""

from pkan.dcatapde.content.dcat_catalog import IDCATCatalog
from pkan.dcatapde.content.dcat_collectioncatalog import IDCATCollectionCatalog
from pkan.dcatapde.content.foaf_agent import IFOAFAgent
from pkan.dcatapde.io.rdf.dexterity import Dexterity2Surf
from pkan.dcatapde.io.rdf.interfaces import ISurfSession
from zope.component import adapter

import surf


class FOAF2Surf(Dexterity2Surf):
    """Dexterity implementation of the Object2Surf."""

    adapter(IFOAFAgent, ISurfSession)

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


class CollectionCatalog2Surf(Dexterity2Surf):
    """Dexterity implementation of the Object2Surf."""

    adapter(IDCATCollectionCatalog, ISurfSession)

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
