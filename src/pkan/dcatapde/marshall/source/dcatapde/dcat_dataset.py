# -*- coding: utf-8 -*-
"""DCAT-AP.de Catalog entity marshaller"""

from pkan.dcatapde.content.dcat_dataset import IDCATDataset
from pkan.dcatapde.marshall.source.dcatapde.dcat2rdf import DCAT2RDF
from pkan.dcatapde.marshall.source.dcatapde.interfaces import IDataset2RDF
from pkan.dcatapde.marshall.target.interfaces import IRDFMarshallTarget
from zope.component import adapter
from zope.interface import implementer


@implementer(IDataset2RDF)
@adapter(IDCATDataset, IRDFMarshallTarget)
class DCATDataset2RDF(DCAT2RDF):
    """Marshaller DCAT-AP.de Catalogs."""

    _namespace = 'dcat'
    _ns_class = 'dataset'

    @property
    def properties(self):
        """Return properties.

        :return:
        """
        result = super(DCATDataset2RDF, self).properties
        return result

    @property
    def contained(self):
        """Return all contained items.

        :return:
        """
        result = {}
        if self.context.isPrincipiaFolderish:
            for item in self.context.values():
                result['dcat:distribution'] = item
        return result

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        related = super(DCATDataset2RDF, self).referenced
        # related['dct:publisher'] = self.context.publisher.to_object
        return related
