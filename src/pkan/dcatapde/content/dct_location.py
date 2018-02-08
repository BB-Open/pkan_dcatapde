# -*- coding: utf-8 -*-
"""DCTLocation Content Type."""

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope import schema
from zope.interface import implementer


class IDCTLocation(model.Schema):
    """Marker interface and DX Python Schema for DCTLocation."""

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


@implementer(IDCTLocation)
class DCTLocation(Item, DCATMixin):
    """DCTLocation Content Type."""

    portal_type = constants.CT_DCT_LOCATION
    _namespace = 'dct'
    _ns_class = 'location'

    dct_title = I18NTextProperty(IDCTLocation['dct_title'])
    dct_description = I18NTextProperty(IDCTLocation['dct_description'])

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


class DCTLocationDefaultFactory(DexterityFactory):
    """Custom DX factory for DCTLocation."""

    def __init__(self):
        self.portal_type = constants.CT_DCT_LOCATION

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api import dct_location
        data, errors = dct_location.clean(**kw)

        return super(
            DCTLocationDefaultFactory,
            self,
        ).__call__(*args, **data)
