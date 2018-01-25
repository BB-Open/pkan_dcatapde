# -*- coding: utf-8 -*-
"""Marshaller module."""

from pkan.dcatapde.io.rdf.interfaces import IGenericObject2Surf
from pkan.dcatapde.io.rdf.interfaces import IObject2Surf
from pkan.dcatapde.io.rdf.interfaces import ISurfResourceModifier
from pkan.dcatapde.io.rdf.interfaces import ISurfSession
from plone.api.portal import get_tool
from Products.CMFCore.interfaces._tools import ITypesTool
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.component import subscribers
from zope.interface import implementer
from zope.interface import Interface

import surf


DEBUG = True


class RDFMarshaller(object):
    """RDF Marshaller, used as a component by Products.Marshaller.

    Marshals content types instances into RDF format.
    """

    _store = None

    @property
    def store(self):
        """Factory for store objects."""
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

    def marshall_inner(self, instance, **kwargs):
        """Marshall the rdf data to xml representation."""
        session = surf.Session(self.store)

        obj2surf = queryMultiAdapter(
            (instance, session),
            interface=IObject2Surf,
        )

        self.store.reader.graph.bind(
            obj2surf.prefix,
            obj2surf.namespace,
            override=False,
        )
        endLevel = kwargs.get('endLevel', 3)
        self.resource = obj2surf.write(endLevel=endLevel, marshaller=self)

    def marshall(self, instance, **kwargs):
        """Marshall the rdf data to xml representation."""
        self.marshall_inner(instance, **kwargs)

        data = self.store.reader.graph.serialize(format='pretty-xml')

        content_type = 'text/xml; charset=UTF-8'

        return (content_type, len(data), data)

    def marshall_graph(self, instance, **kwargs):
        """Marshall the rdf data to xml representation."""
        self.marshall_inner(instance, **kwargs)

#        data = self.store.reader.graph

        return self.resource


@implementer(IGenericObject2Surf)
@adapter(Interface, ISurfSession)
class GenericObject2Surf(object):
    """Generic implementation of IObject2Surf

    This is meant to be subclassed and not used directly.
    """

    _resource = None    # stores the surf resource
    _namespace = None   # stores the namespace for this resource
    _prefix = None

    def __init__(self, context, session):
        self.context = context
        self.session = session

    @property
    def prefix(self):
        """Prefix."""
        if self._prefix is None:
            raise NotImplementedError

        return self._prefix

    @property
    def portalType(self):
        """Portal type."""
        return self.context.__class__.__name__

    @property
    def namespace(self):
        """Namespace."""
        if self._namespace is not None:
            return self._namespace

        ttool = get_tool(self.context, 'portal_types')
        ptype = self.context.portal_type
        ns = {
            self.prefix: '{0}#'.format(ttool[ptype].absolute_url()),
        }
        surf.ns.register(**ns)
        self._namespace = getattr(surf.ns, self.prefix.upper())

        return self._namespace

    @property
    def subject(self):
        """Subject; will be inserted as rdf:about."""
        return '{0}#{1}'.format(self.context.absolute_url(), self.rdfId)

    @property
    def rdfId(self):
        """RDF id; will be inserted as rdf:id."""
        return self.context.getId().replace(' ', '')

    @property
    def resource(self, **kwds):
        """Factory for a new Surf resource."""
        if self._resource is not None:
            return self._resource

        try:
            # pull a new resource from the surf session
            resource = self.session.get_class(
                self.namespace[self.portalType])(self.subject)
        except Exception:
            # import pdb; pdb.set_trace()

            if DEBUG:
                raise
            # logger.exception('RDF marshaller error:')

            return None

        resource.bind_namespaces([self.prefix])
        resource.session = self.session
        self._resource = resource

        return resource

    def modify_resource(self, resource, *args, **kwds):
        """We allow modification of resource here."""
        return resource

    def write(self, *args, **kwds):
        """Write its resource into the session."""
        if self.resource is None:
            raise ValueError

        # we modify the resource and then allow subscriber plugins to modify it
        resource = self.modify_resource(self.resource, *args, **kwds)

        for modifier in subscribers([self.context], ISurfResourceModifier):
            modifier.run(resource, *args, **kwds)

        resource.update()
        resource.save()

        return resource


@adapter(ITypesTool, ISurfSession)
class PortalTypesUtil2Surf(GenericObject2Surf):
    """IObject2Surf implemention for TypeInformations"""

    _prefix = 'rdfs'
    _namespace = surf.ns.RDFS

    @property
    def portalType(self):
        """Portal type."""
        return u'PloneUtility'

    def modify_resource(self, resource, *args, **kwds):
        """_schema2surf"""
        resource.rdfs_label = (u'Plone PortalTypes Tool', None)
        resource.rdfs_comment = (u'Holds definitions of portal types', None)
        resource.rdf_id = self.rdfId

        return resource
