# -*- coding: utf-8 -*-
"""RDF Marshaller."""

from pkan.dcatapde.marshall.target.interfaces import IRDFMarshallTarget
from zope.interface import implementer

# import rdflib
import surf


surf.namespace.register(dct=surf.ns.DCTERMS)
surf.namespace.register(DCAT='http://www.w3.org/ns/dcat#')


@implementer(IRDFMarshallTarget)
class RDFMarshallTarget(object):
    """RDF Marshaller Target."""

    _store = None
    _resource = None

    @property
    def store(self):
        """Factory for store objects."""
        if self._store is not None:
            return self._store

        store = surf.Store(
            reader='rdflib',
            writer='rdflib',
            rdflib_store='IOMemory',
        )

        store.reader.graph.bind('dc', surf.ns.DC, override=True)
        store.reader.graph.bind('dct', surf.ns.DCTERMS, override=True)
        store.reader.graph.bind('skos', surf.ns.SKOS, override=True)
        store.reader.graph.bind('geo', surf.ns.GEO, override=True)
        store.reader.graph.bind('owl', surf.ns.OWL, override=True)
        store.reader.graph.bind('dcat', surf.ns.DCAT, override=True)
        store.reader.graph.bind('foaf', surf.ns.FOAF, override=True)

        self._store = store

        return store

    @property
    def session(self):
        """A new session for surf"""
        session = surf.Session(self.store)
        return session

    def marshall(self, obj):
        """Factory for a new Surf resource."""
        try:
            surf_ns = getattr(surf.ns, obj.namespace.upper())

            resource_class = self.session.get_class(surf_ns[obj.ns_class])
            resource = resource_class(obj.rdf_about)
        except AttributeError:
            surf_ns = getattr(surf.ns, 'RDF')
            resource_class = self.session.get_class(surf_ns['Literal'])
            resource = resource_class(obj.context.absolute_url())

        resource.bind_namespaces([surf_ns])
        resource.session = self.session

        return resource

    def add_property(self, resource, name, value):
        """Add a property."""
        setattr(resource, name.replace(':', '_'), value)

    def set_link(self, resource, name, other_resource):
        """Link two resources."""
        setattr(resource, name.replace(':', '_'), other_resource.subject)

    def set_links(self, resource, name, other_resources):
        """Link list of resources from resource ."""
        subjects = [i.subject for i in other_resources]
        setattr(resource, name.replace(':', '_'), subjects)
