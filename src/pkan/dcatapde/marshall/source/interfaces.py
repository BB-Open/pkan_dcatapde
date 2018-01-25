# -*- coding: utf-8 -*-
# """ Interfaces """
from pkan.dcatapde.marshall.interfaces import IMarshallSource
from zope.interface import Attribute
from zope.interface import Interface


class IDX2RDF(IMarshallSource):
    """Adapts Dexterity objects to marshall them to RDF"""

    rdf_about = Attribute(u'Each DX object must have an rdf_about URI which identifies it like a primary key')
    namespace = Attribute(u'Each DX Object must have a namespace')
    ns_class = Attribute(u'Each DX Object should have a ns_class (class in a namespace)')


class IDXField2Any(IMarshallSource):
    """Adapts dexterity object field to marshal them"""


class IDXField2RDF(IMarshallSource):
    """Adapts dexterity object field to marshal them to RDF"""

    rdf_about = Attribute(u'Each DX object must have an rdf_about URI which identifies it like a primary key')
    namespace = Attribute(u'Each DX Object must have a namespace')
    ns_class = Attribute(u'Each DX Object should have a ns_class (class in a namespace)')
