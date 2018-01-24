# -*- coding: utf-8 -*-
# """ Interfaces """
from pkan.dcatapde.marshall.interfaces import IMarshallSource
from zope.interface import Attribute
from zope.interface import Interface


class ICatalog2RDF(IMarshallSource):
    """Adapts DCAT Catalog objects to marshal them to RDF"""
