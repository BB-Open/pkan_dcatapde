# -*- coding: utf-8 -*-
"""Recursive crawler through objects and properties for marshalling"""
from pkan.dcatapde.marshall.interfaces import IMarshallSource
from pkan.dcatapde.marshall.source.interfaces import IDXField2Any
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IMarshallSource)
@adapter(Interface, Interface)
class DX2Any(object):
    """
    Default marshaller for dexterity
    """
    def __init__(self, context, marshall_target):
        """
        :param context: Content object to start crawl  
        :param marshall_target: marshalling target e.g. an RDF store
        """
        self.context = context
        self.marshall_target = marshall_target

    @property
    def properties(self):
        """
        Do nothing
        :return: 
        """
        return []

    @property
    def contained(self):
        """
        Return all contained items
        :return: 
        """
        if self.context.isPrincipiaFolderish:
            return self.context.items()
        else:
            return []

    @property
    def referenced(self):
        """
        Return all referenced items
        :return: 
        """
        return []

    def marshall_myself(self):
        """marshall myself"""
        self.marshall_target.marshall(self)

    def marshall_properties(self):
        """marshall properties"""
        for property in self.properties:
            property_marshaller = queryMultiAdapter( (property, self.marshall_target), interface=IDXField2Any)
            if property_marshaller:
                # marshall the property
                property_marshaller.marshall(self)
                self.marshall_target.link_to_property( property_marshaller )

    def marshall_contained(self):
        """marshall contained objects"""
        for obj in self.contained:
            contained_marshaller = queryMultiAdapter( (obj, self.marshall_target), interface=IMarshallSource,
                                                          default = DX2Any)
            if contained_marshaller:
                contained_marshaller.marshall(self)
                self.marshall_target.link_to_contained(contained_marshaller)

    def marshall_references(self):
        """marshall the referenced objects"""
        for obj in self.referenced:
            referenced_marshaller = queryMultiAdapter( (obj, self.marshall_target), interface=IDX2Any,
                                                           default = DX2Any)
            if referenced_marshaller:
                referenced_marshaller.marshall(self)
                self.marshall_target.link_to_referenced(referenced_marshaller)

    def marshall(self):
        """marshall properties, contained items and related items"""
        self.marshall_myself()
        self.marshall_properties()
        self.marshall_references()
        self.marshall_contained()
