# -*- coding: utf-8 -*-
"""DCAT-AP.de Catalog entity marshaller"""
from pkan.dcatapde.content.distribution import IDistribution
from pkan.dcatapde.marshall.source.dcatapde.dcat2rdf import DCAT2RDF
from pkan.dcatapde.marshall.source.dcatapde.interfaces import IDistribution2RDF
from pkan.dcatapde.marshall.target.interfaces import IRDFMarshallTarget
from zope.component import adapter
from zope.interface import implementer


@implementer(IDistribution2RDF)
@adapter(IDistribution, IRDFMarshallTarget)
class Distribution2RDF(DCAT2RDF):
    """
    Marshaller DCAT-AP.de Catalogs
    """

    _namespace = "dcat"
    _ns_class = "distribution"

    @property
    def properties(self):
        """
        Do nothing
        :return: 
        """
        result = super(Distribution2RDF, self).properties
        return result

    @property
    def contained(self):
        """
        Return all contained items
        :return: 
        """
        result = {}
        return result

    @property
    def referenced(self):
        """
        Return all referenced items
        :return: 
        """
        related = super(Distribution2RDF, self).referenced
#        related['dct:publisher'] = self.context.publisher.to_object
        return related
