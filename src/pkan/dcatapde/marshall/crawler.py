# -*- coding: utf-8 -*-
"""Recursive crawler through objects and properties for marshalling"""
from pkan.dcatapde.marshall.interfaces import ICrawler
from pkan.dcatapde.marshall.interfaces import IDX2Any
from pkan.dcatapde.marshall.interfaces import IDXField2Any
from pkan.dcatapde.marshall.interfaces import IMarshallTarget
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ICrawler)
@adapter(Interface, IMarshallTarget)
class Crawler(object):

    def __init__(self, context, marshall_target):
        """
        :param context: Content object to start crawl  
        :param marshall_target: marshalling target e.g. an RDF store
        """
        self.context = context
        self.marshall_target = marshall_target

    def crawl(self):
        # find marshaller for context
        context_marshaller = queryMultiAdapter( (self.context, self.marshall_target), interface=IDX2Any,
                                                 default = DX2Any)
        if context_marshaller:
            # marshall the context
            context_marshaller.marshall()
            # marshall the context properties
            for property in context_marshaller.properties:
                property_marshaller = queryMultiAdapter( (property, self.marshall_target), interface=IDXField2Any)
                if property_marshaller:
                    # marhall the property
                    property_marshaller.marshall(context_marshaller)

            # marhall the contained objects
            for obj in context_marshaller.contained:
                crawler = queryMultiAdapter( (obj, self.marshall_target), interface=ICrawler, default = Crawler)
                crawler.crawl()

            # marhall the referenced objects
            for obj in context_marshaller.referenced:
                crawler = queryMultiAdapter( (obj, self.marshall_target), interface=ICrawler, default = Crawler)
                crawler.crawl()


@implementer(IDX2Any)
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

    def marshall(self):
        """
        Do nothing
        :return: 
        """
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
        return self.context.relatedItems
