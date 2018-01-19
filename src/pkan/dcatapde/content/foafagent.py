# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.api.foafagent import add_foafagent
from pkan.dcatapde.constants import CT_Foafagent
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from zope.interface import implementer

import zope.schema as schema


class IFoafagent(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Foafagent
    """

    # URI of FOAF agent has to be required. Since agents can be referenced from
    # several locations at once without a single fixed URI
    # different access paths could arise
    rdf_about = schema.URI(
         title=_(u'Access URI'),
         required=True
    )


@implementer(IFoafagent)
class Foafagent(Item):
    """
    """
    portal_type = 'foafagent'
    namespace_class = 'foaf:agent'


class FoafagentDefaultFactory(DexterityFactory):

    def __init__(self):
        self.portal_type = CT_Foafagent

    def __call__(self, *args, **kw):
        # TODO: get context and maybe change it
        data = add_foafagent(None, dry_run=True, **kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
