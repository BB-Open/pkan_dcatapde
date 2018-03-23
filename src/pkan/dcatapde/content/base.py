# -*- coding: utf-8 -*-
"""Base Content Types."""
from pkan.dcatapde.structure.interfaces import IStructure
from zope.interface import Interface


class IDCAT(Interface):
    """Marker interface for all DCAT-AP.de Content Types"""


class DCATMixin(object):
    """Catalog Content Type."""

    _index_fields = ['dct_title', 'dct_description']

    def title_for_vocabulary(self):
        """Return a title suitable for vocabulary terms."""
        return self.Title()

    def title_from_title_field(self):
        title = None
        struct = IStructure(self)
        for title_field in struct.title_field:
            try:
                all_titles = getattr(self, title_field)
                if not all_titles:
                    continue
                if isinstance(all_titles, dict):
                    title = unicode(all_titles.items()[0][1])
                elif isinstance(all_titles, list):
                        title = unicode(all_titles[0])
                else:
                    title = unicode(all_titles)
            except KeyError:
                continue
        return title
