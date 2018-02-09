# -*- coding: utf-8 -*-
"""FOAFAgent Content Type."""

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.content.util import I18NField2Unique
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.indexer import indexer
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope.interface import implementer


class IFOAFAgent(model.Schema):
    """Marker interface and Dexterity Python Schema for FOAFAgent."""

    # Mandatory
    # -------------------------------------------------------------------------
    dct_title = I18NTextLine(
        required=True,
        title=i18n.LABEL_DCT_TITLE,
    )

    dct_description = I18NText(
        required=True,
        title=i18n.LABEL_DCT_DESCRIPTION,
    )


@implementer(IFOAFAgent)
class FOAFAgent(Item, DCATMixin):
    """FOAFAgent Content Type."""

    portal_type = constants.CT_FOAF_AGENT
    content_schema = IFOAFAgent
    _namespace = 'foaf'
    _ns_class = 'agent'

    dct_title = I18NTextProperty(IFOAFAgent['dct_title'])
    dct_description = I18NTextProperty(IFOAFAgent['dct_description'])

    def Title(self):
        return unicode(self.dct_title)

    def Description(self):
        return unicode(self.dct_description)


class FOAFAgentDefaultFactory(DexterityFactory):
    """Custom DX factory for FOAFAgent."""

    def __init__(self):
        self.portal_type = constants.CT_FOAF_AGENT

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.foaf_agent import clean_foafagent
        data, errors = clean_foafagent(**kw)

        return super(
            FOAFAgentDefaultFactory,
            self,
        ).__call__(*args, **data)


@indexer(IFOAFAgent)
def dct_title(obj):
    result = I18NField2Unique(obj.dct_title)

    if result is None:
        return ''

    return result


@indexer(IFOAFAgent)
def dct_description(obj):
    result = I18NField2Unique(obj.dct_description)

    if result is None:
        return ''

    return result
