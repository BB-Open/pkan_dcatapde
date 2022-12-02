# -*- coding: utf-8 -*-
"""RDF Backend store"""


import surf

from pkan.dcatapde.structure.namespaces import INIT_NS

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

        store.reader.graph.bind('dc', surf.ns.DC, override=True)
        store.reader.graph.bind('dcterms', surf.ns.DCTERMS, override=True)
        store.reader.graph.bind('skos', surf.ns.SKOS, override=True)
        store.reader.graph.bind('geo', surf.ns.GEO, override=True)
        store.reader.graph.bind('owl', surf.ns.OWL, override=True)
        store.reader.graph.bind('dcat', surf.ns.DCAT, override=True)
        store.reader.graph.bind('dcatde', surf.ns.DCATDE, override=True)
        store.reader.graph.bind('schema', surf.ns.SCHEMA, override=True)
        store.reader.graph.bind('foaf', surf.ns.FOAF, override=True)
        store.reader.graph.bind('adms', surf.ns.ADMS, override=True)

        self._store = store

        return store

    def marshall_inner(self, instance, **kwargs):
        """Marshall the rdf data to xml representation."""
        session = surf.Session(self.store)
        assert(session)

        # obj2surf = queryMultiAdapter(
        #     (instance, session), interface=IObject2Surf
        # )

        # self.store.reader.graph.bind(
        #    obj2surf.prefix,
        #    obj2surf.namespace,
        #    override=False,
        # )
        # endLevel = kwargs.get('endLevel', 3)
        # self.resource = obj2surf.write(endLevel=endLevel, marshaller=self)

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
