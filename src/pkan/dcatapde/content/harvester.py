# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IHarvester(model.Schema):
    ''' Marker interfce and Dexterity Python Schema for Harvester
    '''

    url = schema.URI(title=_(u'Harvesting Source'),
                     required=True)

    type = schema.Choice(vocabulary='pkan.dcatapde.HarvestingVocabulary',
                         title=_(u'Schema Type'),
                         required=True,
                         )


@implementer(IHarvester)
class Harvester(Container):
    '''
    '''
