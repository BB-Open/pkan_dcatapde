# -*- coding: utf-8 -*-
"""DCAT-AP.de Catalog entity marshaller"""

from pkan.dcatapde.content.dcat_catalog import IDCATCatalog
from pkan.dcatapde.marshall.source.dcatapde.dcat2rdf import DCAT2RDF
from pkan.dcatapde.marshall.source.dcatapde.interfaces import ICatalog2RDF
from pkan.dcatapde.marshall.target.interfaces import IRDFMarshallTarget
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
        related['dct:publisher'] = self.context.dct_publisher.to_object
        if self.context.dct_license:
            related['dct:license'] = self.context.dct_license.to_object
        if self.context.dct_spatial:
            related['dct:spatial'] = self.context.dct_spatial.to_object
        return related
