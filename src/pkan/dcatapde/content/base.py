# -*- coding: utf-8 -*-
"""Base Content Types."""
from plone.api import portal
from plone.app.content.interfaces import INameFromTitle
from zope.interface import implementer

import surf


class INameFromDCTTitle(INameFromTitle):
    """Get name from catalog title."""

    def title(self):
        """Return a processed title."""


@implementer(INameFromDCTTitle)
class NameFromDCTTitle(object):
    """Get name from catalog title."""

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        if not self.context.dct_title:
            return ''
        if isinstance(self.context.dct_title, unicode):
            return self.context.dct_title
        # Get title from i18nfield
        default_language = portal.get_default_language()[:2]
        if default_language in self.context.dct_title:
            return self.context.dct_title[default_language]
        else:
            current_language = portal.get_current_language()[:2]
            if current_language in self.context.dct_title:
                return self.context.dct_title[current_language]

        return self.context.dct_title[self.context.dct_title.keys()[0]]


class DCATMixin(object):
    """Catalog Content Type."""

    _namespace = None
    _ns_class = None
    _index_fields = ['dct_title', 'dct_description']

    @property
    def namespace_class(self):
        """The complete namespace class name in rdflib notation"""
        return self._namespace.lower() + ':' + self._ns_class.lower()

    @property
    def surf_class(self):
        """The namespace class for SURF from surf.ns"""
        # Namespace MUST BE upper
        surf_ns = self._namespace.upper()
        # Class MUST BE lower
        surf_class = self._ns_class.lower()
        return getattr(surf.ns, surf_ns)[surf_class]

    def title_for_vocabulary(self):
        """Return a title suitable for vocabulary terms."""
        return self.Title()
