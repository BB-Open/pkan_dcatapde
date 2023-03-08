# -*- coding: utf-8 -*-
"""DCTMediaTypeOrExtent Content Type."""

from plone.dexterity.content import Item
from plone.indexer.decorator import indexer
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
        required=False,
        title=i18n.LABEL_RDFS_ISDEFINEDBY,
    )

    skos_inScheme = schema.URI(
        description=i18n.HELP_SKOS_INSCHEME,
        required=False,
        title=i18n.LABEL_SKOS_INSCHEME,
    )


@implementer(IDCTMediaTypeOrExtent)
class DCTMediaTypeOrExtent(Item, DCATMixin):
    """DCTMediatypeorextent Content Type."""

    portal_type = constants.CT_DCT_MEDIATYPEOREXTENT
    content_schema = IDCTMediaTypeOrExtent
    _namespace = 'dct'
    _ns_class = 'MediaTypeOrExtent'

    dct_title = I18NTextProperty(IDCTMediaTypeOrExtent['dct_title'])
    dct_description = I18NTextProperty(
        IDCTMediaTypeOrExtent['dct_description'],
    )

    def Title(self):
        try:
            return self.dct_title[u'deu']
        except KeyError:
            key = list(self.dct_title.keys())[0]
            return self.dct_title[key]

    def Description(self):
        return self.desc_from_desc_field()

    def title_for_vocabulary(self):
        """Return a title suitable for vocabulary terms."""
        return self.Title()


@indexer(IDCTMediaTypeOrExtent)
def DCTMediaTypeOrExtent_dct_title(object, **kw):
    try:
        return object.dct_title[u'deu']
    except KeyError:
        try:
            return object.dct_title[u'de']
        except KeyError:
            return object.dct_title
