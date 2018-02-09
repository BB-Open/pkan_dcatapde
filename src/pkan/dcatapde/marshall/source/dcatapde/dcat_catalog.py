# -*- coding: utf-8 -*-
"""DCAT-AP.de Catalog entity marshaller"""

from pkan.dcatapde.content.dcat_catalog import IDCATCatalog
from pkan.dcatapde.marshall.source.dcatapde.dcat2rdf import DCAT2RDF
from pkan.dcatapde.marshall.source.dcatapde.interfaces import ICatalog2RDF
from pkan.dcatapde.marshall.target.interfaces import IRDFMarshallTarget
from plone.api import content
from zope.component import adapter
from zope.interface import implementer


@implementer(ICatalog2RDF)
@adapter(IDCATCatalog, IRDFMarshallTarget)
class DCATCatalog2RDF(DCAT2RDF):
    """Marshaller DCAT-AP.de Catalogs."""

    @property
    def properties(self):
        """Return properties.

        :return:
        """
        result = super(DCATCatalog2RDF, self).properties
        return result

    @property
    def contained(self):
        """Return all contained items.

        :return:
        """
        result = {}
        if self.context.isPrincipiaFolderish:
            for item in self.context.values():
                result['dcat:dataset'] = item
        return result

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        related = super(DCATCatalog2RDF, self).referenced
        related['dct:publisher'] = content.get(UID=self.context.dct_publisher)
        if self.context.dct_license:
            related['dct:license'] = content.get(UID=self.context.dct_license)
        if self.context.dct_spatial:
            related['dct:spatial'] = content.get(UID=self.context.dct_spatial)
        return related
