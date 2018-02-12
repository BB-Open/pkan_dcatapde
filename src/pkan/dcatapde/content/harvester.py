# -*- coding: utf-8 -*-
"""Harvester Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.api.harvester_field_config import add_harvester_field_config
from pkan.dcatapde.constants import CT_HARVESTER
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
        title=_(u'Harvesting target'),
        description=_(
            u'The Harvesting target chooses the output processor for the '
            u'harvested data. Here one can chose if the imported triples were '
            u'added to common catalogs section (default), or if the '
            u'harvested data is a controlled vacabulary e.g. Licenses from '
            u'dcat-ap.de that should be imported into the licenses folder'
            u'Not yet implemented! Choose "default"!',
        ),
        vocabulary='pkan.dcatapde.HarvestingVocabulary',
    )

    data_type = schema.Choice(
        required=True,
        title=_(u'Processor/Filter'),
        description=_(
            u'The processor depends on the sematic of the data and may be '
            u'specific to a certain data provider or data format e.g. OGD.'
            u'Currently only "Potsdam" is available. If unsure choose "RDF"',
        ),
        vocabulary='pkan.dcatapde.DataTypeVocabulary',
    )

    source_type = schema.Choice(
        required=True,
        title=_(u'Source Format'),
        description=_(
            u'Transport format of the source. Usually this will be a RDF '
            u'variant like (JSON-LD, XML, Turtle), or a generic '
            u'source like "JSON generic"',
        ),
        vocabulary='pkan.dcatapde.SourceTypeVocabulary',
    )


@implementer(IHarvester)
class Harvester(Container):
    """Harvester Content Type."""


class HarvesterDefaultFactory(DexterityFactory):
    """Custom DX factory for Harvester."""

    def __init__(self):
        self.portal_type = CT_HARVESTER

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.harvester import clean_harvester
        data, errors = clean_harvester(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        # raises AttributeError
        # Fix: Solve Attribute Error
        # add_harvester_field_config(folder)

        return folder


def add_field_config(object, event):
    add_harvester_field_config(object)
