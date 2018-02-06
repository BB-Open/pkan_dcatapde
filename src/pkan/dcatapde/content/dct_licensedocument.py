# -*- coding: utf-8 -*-
"""DCTLicenseDocument Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.content.base import DCATMixin
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from zope import schema
from zope.interface import implementer


class IDCTLicenseDocument(model.Schema):
    """Marker interface and DX Python Schema for DCTLicenseDocument."""

    dct_title = I18NTextLine(
        required=True,
        title=_(u'Title'),
    )

    dct_description = I18NText(
        required=False,
        title=_(u'Description'),
    )

    rdfs_isDefinedBy = schema.URI(
        required=True,
        title=_(u'Definition URI'),
    )

    adms_identifier = schema.TextLine(
        required=True,
        title=_(u'Identifier'),
    )


@implementer(IDCTLicenseDocument)
class DCTLicenseDocument(Item, DCATMixin):
    """DCTLicenseDocument Content Type."""

    portal_type = CT_DCT_LICENSEDOCUMENT
    _namespace = 'dct'
    _ns_class = 'licensedocument'


class DCTLicenseDocumentDefaultFactory(DexterityFactory):
    """Custom DX factory for DCTLicenseDocument."""

    def __init__(self):
        self.portal_type = CT_DCT_LICENSEDOCUMENT

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.dct_licensedocument import \
            clean_dct_licensedocument
        data, errors = clean_dct_licensedocument(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
