# -*- coding: utf-8 -*-
"""FOAFAgent Content Type."""

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope.interface import implementer

import zope.schema as schema


class IFOAFagent(model.Schema):
    """Marker interface and Dexterity Python Schema for FOAFagent."""

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

    rdf_about = schema.URI(
        required=True,
        title=i18n.LABEL_RDF_ABOUT,
    )


@implementer(IFOAFagent)
class FOAFagent(Item, DCATMixin):
    """FOAFAgent Content Type."""

    portal_type = constants.CT_FOAF_AGENT
    _namespace = 'foaf'
    _ns_class = 'agent'

    dct_title = I18NTextProperty(IFOAFagent['dct_title'])
    dct_description = I18NTextProperty(IFOAFagent['dct_description'])

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
        from pkan.dcatapde.api.foafagent import clean_foafagent
        data, errors = clean_foafagent(**kw)

        return super(
            FOAFAgentDefaultFactory,
            self,
        ).__call__(*args, **data)
