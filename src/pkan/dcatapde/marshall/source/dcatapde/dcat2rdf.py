# -*- coding: utf-8 -*-
"""DCAT-AP.de base entity marshaller"""

from pkan.dcatapde.marshall.source.dx2any import DX2Any
from pkan.dcatapde.marshall.source.dx2any import DXField2Any


class DCAT2RDF(DX2Any):
    """Marshaller for DCAT-AP.de."""

    @property
    def rdf_about(self):
        """Each DX object should have an rdf_about URI.

        This URI identifies it like a primary key.
        If not we generate an URI from the absolute URL.
        """
        if getattr(self.context, 'rdf_about', None) and \
                self.context.rdf_about:
            return self.context.rdf_about
        if getattr(self.context, 'rdfs_isDefinedBy', None) and \
                self.context.rdfs_isDefinedBy:
            return self.context.rdfs_isDefinedBy
        return self.context.absolute_url()

    @property
    def namespace(self):
        """Each DX Object should have a namspace.
        """
        return self.context._namespace

    @property
    def ns_class(self):
        """Each DX Object should have a ns_class (class in a namespace).
        """
        return self.context._ns_class


class DCATField2RDF(DXField2Any):
    """Marshaller for DCAT-AP.de."""

    @property
    def rdf_about(self):
        """Each DX object should have an rdf_about URI.

        This URI identifies it like a primary key.
        If not we generate an URI from the absolute URL.
        """
        return None

    @property
    def namespace(self):
        """Each DX Object should have a namspace.
        """
        return self.context._namespace

    @property
    def ns_class(self):
        """Each DX Object should have a ns_class (class in a namespace).
        """
        return self.context._ns_class
