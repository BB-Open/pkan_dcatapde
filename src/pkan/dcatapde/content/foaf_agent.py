# -*- coding: utf-8 -*-
"""FOAFAgent Content Type."""

from plone.dexterity.content import Item
from plone.indexer import indexer
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
from pkan.dcatapde.content.util import I18NField2Unique


class IFOAFAgent(model.Schema, IDCAT):
    """Marker interface and Dexterity Python Schema for FOAFAgent."""

    # Mandatory
    # -------------------------------------------------------------------------
    foaf_name = I18NTextLine(
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


@implementer(IFOAFAgent)
class FOAFAgent(Item, DCATMixin):
    """FOAFAgent Content Type."""

    portal_type = constants.CT_FOAF_AGENT
    content_schema = IFOAFAgent
    _namespace = 'foaf'
    _ns_class = 'Agent'

    foaf_name = I18NTextProperty(IFOAFAgent['foaf_name'])
    dct_description = I18NTextProperty(IFOAFAgent['dct_description'])

    def Title(self):
        return self.title_from_title_field()

    def Description(self):
        return self.desc_from_desc_field()


@indexer(IFOAFAgent)
def foaf_name(obj):
    result = I18NField2Unique(obj.foaf_name)

    if result is None:
        return ''

    return result


@indexer(IFOAFAgent)
def dct_description(obj):
    result = I18NField2Unique(obj.dct_description)

    if result is None:
        return ''

    return result
