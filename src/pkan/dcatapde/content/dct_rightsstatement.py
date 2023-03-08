# -*- coding: utf-8 -*-
"""DCTRightsStatement Content Type."""

from plone.dexterity.content import Item
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope import schema
from zope.interface import implementer

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.content.base import IDCAT


class IDCTRightsStatement(model.Schema, IDCAT):
    """Marker interface and DX Python Schema for DCTRightsStatement."""

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


#    adms_identifier = schema.TextLine(
#        required=True,
#        title=i18n.LABEL_ADMS_IDENTIFIER,
#    )


@implementer(IDCTRightsStatement)
class DCTRightsStatement(Item, DCATMixin):
    """DCTRightsStatement Content Type."""

    portal_type = constants.CT_DCT_RIGHTSSTATEMENT
    content_schema = IDCTRightsStatement
    _namespace = 'dct'
    _ns_class = 'RightsStatement'

    dct_title = I18NTextProperty(IDCTRightsStatement['dct_title'])
    dct_description = I18NTextProperty(IDCTRightsStatement['dct_description'])

    def Title(self):
        return self.title_from_title_field()

    def Description(self):
        return self.desc_from_desc_field()

    def title_for_vocabulary(self):
        """Return a title suitable for vocabulary terms."""
        return u'{title} ({url})'.format(
            title=self.Title(),
            url=self.rdfs_isDefinedBy,
        )
