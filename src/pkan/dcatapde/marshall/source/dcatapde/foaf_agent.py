# -*- coding: utf-8 -*-
"""DCAT-AP.de Catalog entity marshaller"""

from pkan.dcatapde.content.foaf_agent import IFOAFAgent
from pkan.dcatapde.marshall.interfaces import IMarshallSource
from pkan.dcatapde.marshall.source.dcatapde.dcat2rdf import DCAT2RDF
from pkan.dcatapde.marshall.target.interfaces import IRDFMarshallTarget
from zope.component import adapter
from zope.interface import implementer


@implementer(IMarshallSource)
@adapter(IFOAFAgent, IRDFMarshallTarget)
class FOAFAgent2RDF(DCAT2RDF):
    """Marshaller DCAT-AP.de FOAFAgents."""

    _blacklist = ['rdf_about']

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        related = super(FOAFAgent2RDF, self).referenced
        return related
