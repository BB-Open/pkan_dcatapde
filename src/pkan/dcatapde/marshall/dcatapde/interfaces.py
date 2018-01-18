# -*- coding: utf-8 -*-
# """ Interfaces """
from pkan.dcatapde.marshall.interfaces import IDX2RDF
from zope.interface import Attribute
from zope.interface import Interface


class ICatalog2RDF(IDX2RDF):
    """Adapts DCAT Catalog objects to marshal them to RDF"""
