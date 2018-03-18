# -*- coding: utf-8 -*-
"""SKOSConceptScheme Content Type."""

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.content.base import IDCAT
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope import schema
from zope.interface import implementer


class ISKOSConceptScheme(model.Schema, IDCAT):
    """Marker interface and DX Python Schema for SKOSConceptScheme."""

    # Mandatory
    # -------------------------------------------------------------------------
    dct_title = I18NTextLine(
        required=True,
        title=i18n.LABEL_DCT_TITLE,
    )

    dct_description = I18NText(
        required=False,
        title=i18n.LABEL_DCT_DESCRIPTION,
    )

    rdfs_isDefinedBy = schema.URI(
        required=False,
        title=i18n.LABEL_RDFS_ISDEFINEDBY,
    )


@implementer(ISKOSConceptScheme)
class SKOSConceptScheme(Item, DCATMixin):
    """SKOSConceptScheme Content Type."""

    portal_type = constants.CT_SKOS_CONCEPTSCHEME
    _namespace = 'skos'
    _ns_class = 'conceptscheme'

    dct_title = I18NTextProperty(ISKOSConceptScheme['dct_title'])
    dct_description = I18NTextProperty(ISKOSConceptScheme['dct_description'])

    def Title(self):
        return self.title_from_title_field()

    def Description(self):
        return unicode(self.dct_description)


class SKOSConceptSchemeDefaultFactory(DexterityFactory):
    """Custom DX factory for SKOSConceptScheme."""

    def __init__(self):
        self.portal_type = constants.CT_SKOS_CONCEPTSCHEME

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.skos_conceptscheme import \
            clean_skos_conceptscheme
        data, errors = clean_skos_conceptscheme(**kw)

        return super(
            SKOSConceptSchemeDefaultFactory,
            self,
        ).__call__(*args, **data)
