# -*- coding: utf-8 -*-
import surf
from pkan.dcatapde.marshall.target.interfaces import IRDFMarshallTarget
from zope.interface import implementer


@implementer(IRDFMarshallTarget)
class RDFMarshallTarget(object):

    _store = None
    _resource = None

    @property
    def store(self):
        """Factory for store objects
        """

        if self._store is not None:
            return self._store

        store = surf.Store(reader='rdflib', writer='rdflib',
                           rdflib_store='IOMemory')

        store.reader.graph.bind('dc', surf.ns.DC, override=True)
        store.reader.graph.bind('dcterms', surf.ns.DCTERMS, override=True)
        store.reader.graph.bind('skos', surf.ns.SKOS, override=True)
        store.reader.graph.bind('geo', surf.ns.GEO, override=True)
        store.reader.graph.bind('owl', surf.ns.OWL, override=True)
        store.reader.graph.bind('dcat', surf.ns.DCAT, override=True)
        store.reader.graph.bind('schema', surf.ns.SCHEMA, override=True)
        store.reader.graph.bind('foaf', surf.ns.FOAF, override=True)

        self._store = store

        return store


    @property
    def session(self):
        """A new session for surf"""
        session = surf.Session(self.store)
        return session

    def marshall(self, obj):
        """ Factory for a new Surf resource """

        surf_ns = getattr(surf.ns, obj.namespace.upper())

        self.resource = self.session.get_class(surf_ns[obj.ns_class])(obj.rdf_about)

        self.resource.bind_namespaces([surf_ns])
        self.resource.session = self.session


    def link_to_property(self):
        """Link to a property"""

    def link_to_contained(self):
        """Link to a contained object"""

    def link_to_referenced(self):
        """Link to a referenced object"""