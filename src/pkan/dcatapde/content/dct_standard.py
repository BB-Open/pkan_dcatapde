# -*- coding: utf-8 -*-
"""DCTStandard Content Type."""

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


class IDCTStandard(model.Schema, IDCAT):
    """Marker interface and DX Python Schema for DCTStandard."""

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
        required=True,
        title=i18n.LABEL_RDFS_ISDEFINEDBY,
    )


@implementer(IDCTStandard)
class DCTStandard(Item, DCATMixin):
    """DCTStandard Content Type."""

    portal_type = constants.CT_DCT_STANDARD
    content_schema = IDCTStandard
    _namespace = 'dct'
    _ns_class = 'standard'

    dct_title = I18NTextProperty(IDCTStandard['dct_title'])
    dct_description = I18NTextProperty(IDCTStandard['dct_description'])

    def Title(self):
        return unicode(self.dct_title)

    def Description(self):
        return unicode(self.dct_description)

    def title_for_vocabulary(self):
        """Return a title suitable for vocabulary terms."""
        return u'{title} ({url})'.format(
            title=self.Title(),
            url=self.rdfs_isDefinedBy,
        )


class DCTStandardDefaultFactory(DexterityFactory):
    """Custom DX factory for DCTStandard."""

    def __init__(self):
        self.portal_type = constants.CT_DCT_STANDARD

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.dct_standard import clean
        data, errors = clean(**kw)

        return super(
            DCTStandardDefaultFactory,
            self,
        ).__call__(*args, **data)
