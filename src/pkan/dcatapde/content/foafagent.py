# -*- coding: utf-8 -*-
"""FOAFAgent Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_Foafagent
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from zope.interface import implementer

import zope.schema as schema


class IFoafagent(model.Schema):
    """Marker interfce and Dexterity Python Schema for Foafagent."""

    dct_title = I18NTextLine(
        required=True,
        title=_(u'Title'),
    )

    dct_description = I18NText(
        required=True,
        title=_(u'Description'),
    )

    # URI of FOAF agent has to be required. Since agents can be referenced from
    # several locations at once without a single fixed URI
    # different access paths could arise
    rdf_about = schema.URI(
        required=True,
        title=_(u'Access URI'),
    )


@implementer(IFoafagent)
class Foafagent(Item):
    """FOAFAgent Content Type."""

    portal_type = 'foafagent'
    namespace_class = 'foaf:agent'


class FoafagentDefaultFactory(DexterityFactory):
    """Custom DX factory for FOAFAgent."""

    def __init__(self):
        self.portal_type = CT_Foafagent

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.foafagent import clean_foafagent
        data, errors = clean_foafagent(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
