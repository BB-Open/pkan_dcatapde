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

    def marshall_as_literal(self):
        if not self.structure.literal_field:
            return None
        property_name = self.structure.literal_field
        struct_info = self.structure.properties[property_name]
        property_value = getattr(self.context, property_name)
        if not property_value:
            # do not marshall empty fields
            return []
        if struct_info['type'] != list:
            property_list = [property_value]
        else:
            property_list = property_value

        values = []
        for property in property_list:
            property_marshaller = queryMultiAdapter(
                (self.context, property, self.marshall_target),
                interface=IMarshallSource,
            )

            if property_marshaller:
                # let the adapter marshall the property
                marshalled_property = property_marshaller.marshall(self)
                return marshalled_property
            else:
                # No adapter can be found, convert the field value
                # to a string.
                value = str(property)
                values.append(value)
        return values

    def marshall_property(self, rdf_name, property):
        # Marshall a property that contains a single value.
        # At first check for an available filed_name adapter to do this.
        field_name_property_marshaller = queryMultiAdapter(
            (self.context, self.marshall_target),
            interface=IMarshallSource,
            name=rdf_name,
        )
        if field_name_property_marshaller:
            marshalled_property = field_name_property_marshaller.marshall(self)
        else:
            # if no field_name_adapter is available
            # check for a more general property adapter
            property_marshaller = queryMultiAdapter(
                (self.context, property, self.marshall_target),
                interface=IMarshallSource,
            )

            if property_marshaller:
                # let the adapter marshall the property
                marshalled_property = property_marshaller.marshall(self)
            else:
                # No adapter can be found, convert the field value
                # to a string.
                if property is None:
                    return
                marshalled_property = str(property)
        if marshalled_property is not None:
            self.marshall_target.add_property(
                self.resource,
                rdf_name,
                marshalled_property,
            )

    def marshall_listproperty(self, rdf_name, listproperty):
        # handle a list property. This code is unstable.
        # May fail if the property marshaller if a list element returns
        # a list of results.
        if listproperty is None:
            return
        values = []
        for property in listproperty:
            property_marshaller = queryMultiAdapter(
                (self.context, property, self.marshall_target),
                interface=IMarshallSource,
            )
            if property_marshaller:
                # let the adapter marshall the property
                marshalled_property = property_marshaller.marshall(self)
                self.marshall_target.add_property(
                    self.resource,
                    rdf_name,
                    marshalled_property,
                )
            else:
                # No adapter can be found, convert the field value
                # to a string.
                value = str(property)
                values.append(value)
        if values:
            self.marshall_target.add_property(
                self.resource,
                rdf_name,
                values,
            )

    def marshall_properties(self):
        """Marshall properties."""
        for property_name in self.structure.properties:
            struct_info = self.structure.properties[property_name]
            property_value = getattr(self.context, property_name)
            # get the rdf_name of the property
            if 'rdf_name' in struct_info:
                rdf_name = struct_info['rdf_name']
            else:
                rdf_name = property_name
            # is the property a list or a single value
            if struct_info['type'] == list:
                self.marshall_listproperty(rdf_name, property_value)
            else:
                self.marshall_property(rdf_name, property_value)

    def marshall_contained(self):
        """Marshall contained objects."""
        for item_name in self.structure.contained:
            resources = []
            try:
                # Do we have a collection?
                items = [item.getObject() for item in ICollection(
                    self.context).results(batch=False)]
            except TypeError as e:
                # if not we have a folder
                items = self.context.values()
            for item in items:
                if item_name == item.portal_type:
                    contained_marshaller = queryMultiAdapter(
                        (item, self.marshall_target),
                        interface=IMarshallSource,
                        default=DX2Any(item, self.marshall_target),
                    )
                    if contained_marshaller:
                        contained_marshaller.marshall()
                        resources.append(contained_marshaller.resource)

            self.marshall_target.set_links(
                self.resource,
                item_name,
                resources,
            )

    def marshall_references(self):
        """Marshall the referenced objects."""
        for ref_name in self.structure.referenced:

            if self.structure.referenced[ref_name]['type'] != list:
                uid = getattr(self.context, ref_name, None)
                if not uid:
                    continue
                uid_list = [uid]
            else:
                uid_list = getattr(self.context, ref_name, None)
                if not uid_list:
                    continue
            resources = []
            for uid in uid_list:
                ref = content.get(UID=uid)
                if not ref:
                    continue
                referenced_marshaller = queryMultiAdapter(
                    (ref, self.marshall_target),
                    interface=IMarshallSource,
                    default=DX2Any(ref, self.marshall_target),
                )
                if referenced_marshaller:
                    # referenced object should be a literal instead of a object
                    literals = referenced_marshaller.marshall_as_literal()
                    if literals is not None:
                        self.marshall_target.add_property(
                            self.resource,
                            ref_name,
                            literals,
                        )
                    else:
                        referenced_marshaller.marshall()
                        resources.append(referenced_marshaller.resource)
            if resources:
                self.marshall_target.set_links(
                    self.resource,
                    ref_name,
                    resources,
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
