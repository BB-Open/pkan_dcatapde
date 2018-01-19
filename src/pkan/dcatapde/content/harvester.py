# -*- coding: utf-8 -*-
from plone.dexterity.factory import DexterityFactory

from pkan.dcatapde import _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from pkan.dcatapde.api.harvester import add_harvester, \
    add_harvester_field_config
from pkan.dcatapde.constants import CT_Harvester


class IHarvester(model.Schema):
    ''' Marker interfce and Dexterity Python Schema for Harvester
    '''

    url = schema.URI(title=_(u'Harvesting Source'),
                     required=True)

    harvesting_type = schema.Choice(vocabulary='pkan.dcatapde.HarvestingVocabulary',
                                    title=_(u'Schema Type'),
                                    required=True,
                                    )


@implementer(IHarvester)
class Harvester(Container):
    '''
    '''


class HarvesterDefaultFactory(DexterityFactory):

    def __init__(self):
        self.portal_type = CT_Harvester

    def __call__(self, *args, **kw):
        # TODO: get context and maybe change it
        data = add_harvester(None, dry_run=True, **kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        add_harvester_field_config(folder)

        return folder