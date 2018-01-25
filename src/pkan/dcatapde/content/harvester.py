# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_Harvester
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from zope.interface import implementer

import zope.schema as schema


class IHarvester(model.Schema):
    ''' Marker interfce and Dexterity Python Schema for Harvester
    '''

    url = schema.URI(title=_(u'Harvesting Source'),
                     required=True)

    harvesting_type = schema.Choice(
        vocabulary='pkan.dcatapde.HarvestingVocabulary',
        title=_(u'Schema Type'),
        required=True,
    )

    preprocessor = schema.Choice(
        vocabulary='pkan.dcatapde.PreprocessorVocabulary',
        title=_(u'Preprocessor'),
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
        from pkan.dcatapde.api.harvester import clean_harvester
        data, errors = clean_harvester(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        # raises AttributeError
        # TODO: Solve Attribute Error
        # add_harvester_field_config(folder)

        return folder
