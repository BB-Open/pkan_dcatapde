# -*- coding: utf-8 -*-
"""DCTLicenseDocument Content Type."""

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


class IDCTLicenseDocument(model.Schema, IDCAT):
    """Marker interface and DX Python Schema for DCTLicenseDocument."""

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

    adms_identifier = schema.TextLine(
        required=True,
        title=i18n.LABEL_ADMS_IDENTIFIER,
    )


@implementer(IDCTLicenseDocument)
class DCTLicenseDocument(Item, DCATMixin):
    """DCTLicenseDocument Content Type."""

    portal_type = constants.CT_DCT_LICENSEDOCUMENT
    content_schema = IDCTLicenseDocument
    _namespace = 'dct'
    _ns_class = 'licensedocument'

    dct_title = I18NTextProperty(IDCTLicenseDocument['dct_title'])
    dct_description = I18NTextProperty(IDCTLicenseDocument['dct_description'])

    def Title(self):
        return self.title_from_title_field()

    def Description(self):
        return unicode(self.dct_description)

    def title_for_vocabulary(self):
        """Return a title suitable for vocabulary terms."""
        return u'{title} ({url})'.format(
            title=self.Title(),
            url=self.rdfs_isDefinedBy,
        )


class DCTLicenseDocumentDefaultFactory(DexterityFactory):
    """Custom DX factory for DCTLicenseDocument."""

    def __init__(self):
        self.portal_type = constants.CT_DCT_LICENSEDOCUMENT

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.dct_licensedocument import \
            clean_dct_licensedocument
        data, errors = clean_dct_licensedocument(**kw)

        return super(
            DCTLicenseDocumentDefaultFactory,
            self,
        ).__call__(*args, **data)
