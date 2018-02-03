# -*- coding: utf-8 -*-
"""DCTMediatypeorextent Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_SCOS_CONCEPTSCHEME
from pkan.dcatapde.content.dcat_catalog import INameFromDCTTitle
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from zope import schema
from zope.interface import implementer


class ISCOSConceptScheme(model.Schema):
    """Marker interface and DX Python Schema for SCOSConceptScheme."""

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
        title=_(u'URI'),
    )


@implementer(ISCOSConceptScheme)
class SCOSConceptScheme(Item):
    """SCOSConceptScheme Content Type."""

    portal_type = 'scos_conceptscheme'
    namespace_class = 'scos:conceptscheme'

    _Title = ''

    def Title(self):
        if not self._Title:
            self._Title = INameFromDCTTitle(self).title
        return self._Title


class SCOSConceptSchemeDefaultFactory(DexterityFactory):
    """Custom DX factory for SCOSConceptScheme."""

    def __init__(self):
        self.portal_type = CT_SCOS_CONCEPTSCHEME

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.dct_mediatypeorextend import \
            clean_dct_mediatypeorextent
        data, errors = clean_dct_mediatypeorextent(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
