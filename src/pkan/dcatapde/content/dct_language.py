# -*- coding: utf-8 -*-
"""DCTLanguage Content Type."""

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


class IDCTLanguage(model.Schema, IDCAT):
    """Marker interface and DX Python Schema for DCTLanguage."""

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

    old_representation = schema.TextLine(
        required=False,
        title=u'2 Letter Representation',
    )

    new_representation = schema.TextLine(
        required=True,
        title=u'3 Letter Representation',
    )

    skos_inScheme = schema.URI(
        description=i18n.HELP_SKOS_INSCHEME,
        required=True,
        title=i18n.LABEL_SKOS_INSCHEME,
        default='http://publications.europa.eu/resource/authority/language'
    )


@implementer(IDCTLanguage)
class DCTLanguage(Item, DCATMixin):
    """DCTLanguage Content Type."""

    portal_type = constants.CT_DCT_LANGUAGE
    content_schema = IDCTLanguage
    _namespace = 'dct'
    _ns_class = 'Language'

    dct_title = I18NTextProperty(IDCTLanguage['dct_title'])
    dct_description = I18NTextProperty(IDCTLanguage['dct_description'])

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
