# -*- coding: utf-8 -*-
"""Mardshaller Interfaces."""

from zope.interface import Attribute
from zope.interface import Interface


class IMarshallSource(Interface):
    """Adapts dexterity objects to marshal them."""

    properties = Attribute(u'Returns the properties that are to be marshalled')
    contained = Attribute(u'Returns the contained content to be marshalled')
    referenced = Attribute(u'Returns the referenced content to be marshalled')

    def marshall(self):
        """Export the contents of the dexterity object elsewhere."""


class IMarshallTarget(Interface):
    """Target to marshall to e.g. RDF, JSON"""

    def marshall(self):
        """Export the contents of the adapted object to the target."""

    def link_to_property(self):
        """Link to a property"""

    def link_to_contained(self):
        """Link to a contained object"""

    def link_to_referenced(self):
        """Link to a referenced object"""
