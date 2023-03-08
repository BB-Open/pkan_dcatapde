# -*- coding: utf-8 -*-
"""RDF Backend store"""

import surf

from pkan.dcatapde.structure.namespaces import INIT_NS
from pkan_config.namespaces import NAMESPACES

surf.namespace.register(**INIT_NS)

DEBUG = True


class RDFStore(object):
    """RDF Store to hold rdf persistently."""

    _store = None

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

        for namespace, uri in NAMESPACES.items():
            store.reader.graph.bind(namespace, uri, override=True)

        self._store = store

        return store

    def marshall_inner(self, instance, **kwargs):
        """Marshall the rdf data to xml representation."""
        session = surf.Session(self.store)
        assert (session)

    def marshall(self, instance, **kwargs):
        """Marshall the rdf data to xml representation."""
        self.marshall_inner(instance, **kwargs)

        data = self.store.reader.graph.serialize(format='pretty-xml')

        content_type = 'text/xml; charset=UTF-8'

        return (content_type, len(data), data)

    def marshall_graph(self, instance, **kwargs):
        """Marshall the rdf data to xml representation."""
        self.marshall_inner(instance, **kwargs)

        # data = self.store.reader.graph

        return self.resource
