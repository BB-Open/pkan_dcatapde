# -*- coding: utf-8 -*-
"""Recursive crawler through objects and properties for marshalling"""
from pkan.dcatapde.io.marshall.interfaces import ICrawler
from pkan.dcatapde.io.marshall.interfaces import IDX2Any
from pkan.dcatapde.io.marshall.interfaces import IDXField2Any
from pkan.dcatapde.io.marshall.interfaces import IMarshallTarget
from zope.component import adapter
from zope.component import getMultiAdapter
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
        context_marshaller = getMultiAdapter( (self.context, self.marshall_target), interface=IDX2Any)
        # marshall the context
        context_marshaller.marshall()
        # marshall the context properties
        for property in context_marshaller.properties:
            property_marshaller = getMultiAdapter( (property, self.marshall_target), interface=IDXField2Any)
            # marhall the property
            property_marshaller.marshall(context_marshaller)

        # marhall the context contained objects
        for obj in context_marshaller.contained:
            ICrawler(obj, self.marshall_target).crawl()
