# -*- coding: utf-8 -*-
"""Base Content Types."""


from zope.interface import Interface


class IDCAT(Interface):
    """Marker interface for all DCAT-AP.de Content Types"""


class DCATMixin(object):
    """Catalog Content Type."""

    _index_fields = ['dct_title', 'dct_description']

    def title_for_vocabulary(self):
        """Return a title suitable for vocabulary terms."""
        return self.Title()
