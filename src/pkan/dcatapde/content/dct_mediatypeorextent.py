# -*- coding: utf-8 -*-
"""Dct_Mediatypeorextent Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DctMediatypeorextent
from pkan.dcatapde.content.catalog import INameFromCatalog
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from zope import schema
from zope.interface import implementer


class IDct_Mediatypeorextent(model.Schema):
    """Marker interfce and DX Python Schema for Dct_Mediatypeorextent."""

    dct_title = I18NTextLine(
        required=True,
        title=_(u'Title'),
    )

    dct_description = I18NText(
        required=False,
        title=_(u'Description'),
    )

    rdf_about = schema.URI(
        required=True,
        title=_(u'Access URI'),
    )


@implementer(IDct_Mediatypeorextent)
class Dct_Mediatypeorextent(Item):
    """Dct_Mediatypeorextent Content Type."""

    portal_type = 'dct_licensedocument'
    namespace_class = 'dct:licensedocument'

    _Title = ''

    def Title(self):
        if not self._Title:
            self._Title = INameFromCatalog(self).title
        return self._Title


class DctMediatypeorextentDefaultFactory(DexterityFactory):
    """Custom DX factory for Dct_Mediatypeorextent."""

    def __init__(self):
        self.portal_type = CT_DctMediatypeorextent

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.dct_mediatypeorextend import \
            clean_dct_mediatypeorextent
        data, errors = clean_dct_mediatypeorextent(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder