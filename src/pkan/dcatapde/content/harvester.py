# -*- coding: utf-8 -*-
"""Harvester Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_Harvester
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from zope.interface import implementer

import zope.schema as schema


class IHarvester(model.Schema):
    """Marker interfce and Dexterity Python Schema for Harvester."""

    url = schema.URI(
        required=True,
        title=_(u'Harvesting Source'),
    )

    harvesting_type = schema.Choice(
        required=True,
        title=_(u'Schema Type'),
        vocabulary='pkan.dcatapde.HarvestingVocabulary',
    )

    preprocessor = schema.Choice(
        required=True,
        title=_(u'Preprocessor'),
        vocabulary='pkan.dcatapde.PreprocessorVocabulary',
    )


@implementer(IHarvester)
class Harvester(Container):
    """Harvester Content Type."""


class HarvesterDefaultFactory(DexterityFactory):
    """Custom DX factory for Harvester."""

    def __init__(self):
        self.portal_type = CT_Harvester

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.harvester import clean_harvester
        data, errors = clean_harvester(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        # raises AttributeError
        # Fix: Solve Attribute Error
        # add_harvester_field_config(folder)

        return folder
