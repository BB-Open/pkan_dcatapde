# -*- coding: utf-8 -*-
# """ Interfaces """
from zope.interface import Attribute
from zope.interface import Interface


class ICrawler(Interface):
    """Recursive generator of Objects and Properties"""


class IMarshallTarget(Interface):
    """Target to marshall to e.g. RDF, JSON"""


class IRDFMarshallTarget(IMarshallTarget):
    """Target to marshall to RDF"""


class IDX2Any(Interface):
    """Base: Adapts dexterity objects to marshal them"""

    properties = Attribute(u'The properties that are to be marshalled')
    contained = Attribute(u'The contained content to be marshalled')


class IDX2RDF(IDX2Any):
    """Adapts dexterity objects to marshal them to RDF"""


class IDXField2Any(Interface):
    """Adapts dexterity object field to marshal them"""


class IDXField2RDF(Interface):
    """Adapts dexterity object field to marshal them to RDF"""
