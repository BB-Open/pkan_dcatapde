# -*- coding: utf-8 -*-
"""DCATAP-DE Interfaces."""

from pkan.dcatapde.marshall.source.interfaces import IDX2RDF


class ICatalog2RDF(IDX2RDF):
    """Adapts DCAT Catalog objects to marshal them to RDF"""


class IDataset2RDF(IDX2RDF):
    """Adapts DCAT Dataset objects to marshal them to RDF"""


class IDistribution2RDF(IDX2RDF):
    """Adapts DCAT Dataset objects to marshal them to RDF"""
