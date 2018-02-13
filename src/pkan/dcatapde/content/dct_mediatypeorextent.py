# -*- coding: utf-8 -*-
"""DCTMediaTypeOrExtent Content Type."""

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


class IDCTMediaTypeOrExtent(model.Schema, IDCAT):
    """Marker interfce and DX Python Schema for DCTMediaTypeOrExtent."""

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


@implementer(IDCTMediaTypeOrExtent)
class DCTMediaTypeOrExtent(Item, DCATMixin):
    """DCTMediatypeorextent Content Type."""

    portal_type = constants.CT_DCT_MEDIATYPEOREXTENT
    content_schema = IDCTMediaTypeOrExtent
    _namespace = 'dct'
    _ns_class = 'mediatypeorextent'

    dct_title = I18NTextProperty(IDCTMediaTypeOrExtent['dct_title'])
    dct_description = I18NTextProperty(
        IDCTMediaTypeOrExtent['dct_description'],
    )

    def Title(self):
        return unicode(self.dct_title)

    def Description(self):
        return unicode(self.dct_description)


class DCTMediaTypeOrExtentDefaultFactory(DexterityFactory):
    """Custom DX factory for DCTMediaTypeOrExtent."""

    def __init__(self):
        self.portal_type = constants.CT_DCT_MEDIATYPEOREXTENT

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.dct_mediatypeorextend import \
            clean_dct_mediatypeorextent
        data, errors = clean_dct_mediatypeorextent(**kw)

        return super(
            DCTMediaTypeOrExtentDefaultFactory,
            self,
        ).__call__(*args, **data)
