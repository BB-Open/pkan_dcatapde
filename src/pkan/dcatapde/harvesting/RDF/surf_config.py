# -*- coding: utf-8 -*-
"""Configuration of surf. Storage, Namespaces and constants"""

import surf


surf.namespace.register(ADMS='http://www.w3.org/ns/adms#')
surf.namespace.register(DCAT='http://www.w3.org/ns/dcat#')
surf.namespace.register(DCATDE='http://dcat-ap.de/def#')

# IMPORTANT surf class definition HAVE TO BE lowercase !!!!!!
SC_DCAT_CATALOG = surf.ns.DCAT['catalog']
SC_DCAT_DATASET = surf.ns.DCAT['dataset']
SC_DCAT_DISTRIBUTION = surf.ns.DCAT['distribution']


class RDFStorage(object):

    def __init__(self):
        """Bring up the SURF/RDFlib infrastructure """
        self.store = surf.Store(
            reader='rdflib',
            writer='rdflib',
            rdflib_store='IOMemory',
        )
        # Get a new surf session
        self.session = surf.Session(self.store)
