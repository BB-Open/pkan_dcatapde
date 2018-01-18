# -*- coding: utf-8 -*-
"""DCAT-AP.de Catalog entity marshaller"""
from pkan.dcatapde.content.catalog import ICatalog
from pkan.dcatapde.marshall.dcatapde.base import DCAT2RDF
from pkan.dcatapde.marshall.interfaces import IDX2Any, IRDFMarshallTarget
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer


@implementer(IDX2Any)
@adapter(ICatalog, IRDFMarshallTarget)
class Catalog2RDF(DCAT2RDF):
    """
    Marshaller DCAT-AP.de Catalogs
    """

    _namespace = "dcat"
    _ns_class = "catalog"

    @property
    def referenced(self):
        """
        Return all referenced items
        :return: 
        """
        related = super(Catalog2RDF, self).referenced
        related.append(self.context.publisher.to_object )
        return related
