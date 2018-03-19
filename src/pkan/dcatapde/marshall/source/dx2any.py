# -*- coding: utf-8 -*-
"""Recursive crawler through objects and properties for marshalling"""

from pkan.dcatapde.marshall.interfaces import IMarshallSource
from pkan.dcatapde.structure.structure import IStructure
from plone.api import content
from plone.app.contenttypes.behaviors.collection import ICollection
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IMarshallSource)
@adapter(Interface, Interface)
class DX2Any(object):
    """Default marshaller for dexterity."""

    _whitelist = []
    _blacklist = []

    def __init__(self, context, marshall_target):
        """Initialization.

        :param context: Content object to start crawl
        :param marshall_target: marshalling target e.g. an RDF store
        """
        self.context = context
        self.marshall_target = marshall_target
        try:
            self.structure = IStructure(self.context)
        except TypeError:
            pass

    def marshall_myself(self):
        """Marshall myself."""
        self.resource = self.marshall_target.marshall(self)

    def marshall_properties(self):
        """Marshall properties."""
        for property_name in self.structure.properties:
            property = getattr(self.context, property_name)
            property_marshaller = queryMultiAdapter(
                (self.context, property, self.marshall_target),
                interface=IMarshallSource,
            )
            if property_marshaller:
                # let the adapter marshall the property
                marshalled_property = property_marshaller.marshall(self)
                self.marshall_target.add_property(
                    self.resource,
                    property_name,
                    marshalled_property,
                )
            else:
                # No adapter can be found, convert the field value to a string.
                value = str(getattr(self.context, property_name))
                self.marshall_target.add_property(
                    self.resource,
                    property_name,
                    value,
                )

    def marshall_contained(self):
        """Marshall contained objects."""
        for item_name in self.structure.contained:
            for item in self.context.values():
                contained_marshaller = queryMultiAdapter(
                    (item, self.marshall_target),
                    interface=IMarshallSource,
                    default=DX2Any(item, self.marshall_target),
                )
                if contained_marshaller:
                    contained_marshaller.marshall()
                    self.marshall_target.set_link(
                        self.resource,
                        item_name,
                        contained_marshaller.resource,
                    )

    def marshall_references(self):
        """Marshall the referenced objects."""
        for item_name in self.structure.referenced:
            uid = getattr(self.context, item_name, None)
            if not uid:
                continue
            item = content.get(UID=uid)
            if not item:
                continue
            referenced_marshaller = queryMultiAdapter(
                (item, self.marshall_target),
                interface=IMarshallSource,
                default=DX2Any(item, self.marshall_target),
            )
            if referenced_marshaller:
                referenced_marshaller.marshall()

                self.marshall_target.set_link(
                    self.resource,
                    item_name,
                    referenced_marshaller.resource,
                )

    def marshall_collection(self):
        """Get content from the collection behavior and marshall it"""
        collection = ICollection(self.context)
        for entry in collection.results():
            item = entry.getObject()
            collection_marshaller = queryMultiAdapter(
                (item, self.marshall_target),
                interface=IMarshallSource,
                default=DX2Any(item, self.marshall_target),
            )
            if collection_marshaller:
                collection_marshaller.marshall()
                rdf_type = IStructure(item).rdf_type
                self.marshall_target.set_link(
                    self.resource,
                    rdf_type,
                    collection_marshaller.resource,
                )

    def marshall(self):
        """Marshall properties, contained items and related items."""
        self.marshall_myself()
        self.marshall_properties()
        self.marshall_references()
        self.marshall_contained()
        # Todo : find better check
        try:
            ICollection(self.context)
            self.marshall_collection()
        except TypeError:
            pass
        self.resource.update()
        self.resource.save()


@implementer(IMarshallSource)
@adapter(Interface, Interface)
class DXField2Any(object):
    """Default marshaller for dexterity."""

    def __init__(self, context, field, marshall_target):
        """Initialization.

        :param context: Content object to start crawl
        :param marshall_target: marshalling target e.g. an RDF store
        """
        self.context = context
        self.field = field
        self.marshall_target = marshall_target

    def marshall_myself(self):
        """Marshall myself."""
        self.resource = self.marshall_target.marshall(self)

    def marshall(self):
        self.marshall_myself()
        # a = IDexterityContent
