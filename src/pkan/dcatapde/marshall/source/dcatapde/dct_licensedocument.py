# -*- coding: utf-8 -*-
"""DCAT-AP.de Catalog entity marshaller"""

from pkan.dcatapde.content.dct_licensedocument import IDCTLicenseDocument
# from pkan.dcatapde.content.foafagent import IFoafagent
from pkan.dcatapde.marshall.interfaces import IMarshallSource
from pkan.dcatapde.marshall.source.dcatapde.dcat2rdf import DCAT2RDF
from pkan.dcatapde.marshall.target.interfaces import IRDFMarshallTarget
from zope.component import adapter
# from zope.interface import Interface
from zope.interface import implementer


@implementer(IMarshallSource)
@adapter(IDCTLicenseDocument, IRDFMarshallTarget)
class Dct_Licensedocument2RDF(DCAT2RDF):
    """Marshaller DCAT-AP.de FOAFAgents."""

    _namespace = 'dct'
    _ns_class = 'licensedocument'
    _blacklist = ['rdf_about']

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        related = super(Dct_Licensedocument2RDF, self).referenced
        return related
