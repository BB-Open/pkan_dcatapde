# -*- coding: utf-8 -*-
"""DCAT-AP.de base entity marshaller"""
from pkan.dcatapde.content.catalog import ICatalog
from pkan.dcatapde.marshall.crawler import DX2Any
from pkan.dcatapde.marshall.interfaces import IDX2Any, IRDFMarshallTarget
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer


class DCAT2RDF(DX2Any):
    """
    Marshaller for DCAT-AP.de 
    """

    _namespace = "dcat"
    _ns_class = "noclass"

    @property
    def rdf_about(self):
        """Each DX object should have an rdf_about URI which identifies it like a primary key
           If not we generate an URI from the absolute URL
        """

        if getattr(self.context,'rdf_about', None):
            return self.context.rdf_about
        return self.context.absolute_url()

    @property
    def namespace(self):
        """Each DX Object should have a namspace . If not the adapter can provide a fallback"""
        if getattr(self.context,'namespace', None):
            return self.context.namespace
        return self._namespace

    @property
    def ns_class(self):
        """Each DX Object should have a ns_class (class in a namespace). If not the adapter can provide a fallback"""
        if getattr(self.context,'ns_class', None):
            return self.context.ns_class
        return self._ns_class

    def marshall(self):
        """
        marshall our class and our rdf:source
        :return: 
        """

        self.resource = self.marshall_target.new_resource(self)

        self.resource.update()
        self.resource.save()




