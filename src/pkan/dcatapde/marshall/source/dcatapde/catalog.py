# -*- coding: utf-8 -*-
"""DCAT-AP.de Catalog entity marshaller"""
from pkan.dcatapde.content.catalog import ICatalog
from pkan.dcatapde.marshall.source.dcatapde.dcat2rdf import DCAT2RDF
from pkan.dcatapde.marshall.source.dcatapde.interfaces import ICatalog2RDF
from pkan.dcatapde.marshall.target.interfaces import IRDFMarshallTarget
from zope.component import adapter
from zope.interface import implementer


@implementer(ICatalog2RDF)
@adapter(ICatalog, IRDFMarshallTarget)
class Catalog2RDF(DCAT2RDF):
    """
    Marshaller DCAT-AP.de Catalogs
    """

    _namespace = "dcat"
    _ns_class = "catalog"

    @property
    def properties(self):
        """
        Do nothing
        :return: 
        """
        result = super(Catalog2RDF, self).properties
        return result

    @property
    def contained(self):
        """
        Return all contained items
        :return: 
        """
        result = {}
        if self.context.isPrincipiaFolderish:
            for item in self.context.values():
                result['dcat:dataset'] = item
        return result

    @property
    def referenced(self):
        """
        Return all referenced items
        :return: 
        """
        related = super(Catalog2RDF, self).referenced
        related['dct:publisher'] = self.context.dct_publisher.to_object
        related['dct:license'] = self.context.dct_license.to_object
        return related
