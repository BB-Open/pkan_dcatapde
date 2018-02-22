# -*- coding: utf-8 -*-
"""Harvester Content Type."""
from DateTime.DateTime import time
from pkan.dcatapde import _
from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.constants import CT_HARVESTER
from pkan.widgets.ajaxselect import AjaxSelectAddFieldWidget
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.memoize import ram
from plone.supermodel import model
from rdflib import Graph
from rdflib.plugins.memory import IOMemory
from zope.interface import implementer

import zope.schema as schema


class IHarvester(model.Schema):
    """Marker interfce and Dexterity Python Schema for Harvester."""

    url = schema.URI(
        required=True,
        title=_(u'Harvesting Source'),
        description=_(u'The URI of the source of data to be harvested.'),
    )

    form.widget(
        'base_object',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_DCAT_CATALOG,
        content_type_title=i18n.LABEL_BASE_OBJECT,
        initial_path='/',
    )
    base_object = schema.Choice(
        required=False,
        title=i18n.LABEL_BASE_OBJECT,
        vocabulary='pkan.dcatapde.vocabularies.DCATCatalog',
        description=i18n.HELP_BASE_OBJECT,
    )

    harvesting_type = schema.Choice(
        # Todo: reset to true when new adapter are added
        required=False,
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

    data_cleaner = schema.Choice(
        required=True,
        title=_(u'Processor/Filter'),
        description=_(
            u'The processor depends on the sematic of the data and may be '
            u'specific to a certain data provider or data format e.g. OGD.'
            u'Currently only "PotsdamCleaner" is available.',
        ),
        vocabulary='pkan.dcatapde.DataCleanerVocabulary',
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


def cache_key(func, self):
    """cache key factory for rdf graph. With timeout 300 seconds
    :param func:
    :param self:
    :return:
    """
    key = u'{0}_{1}'.format(
        time() // 300,
        self.url,
    )
    return key


@implementer(IHarvester)
class Harvester(Container):
    """Harvester Content Type."""

    def __init__(self, *args, **kwargs):

        self._graph = None
        self._rdfstore = None

        super(Harvester, self).__init__(*args, **kwargs)

    @property
    @ram.cache(cache_key)
    def graph(self):
        rdfstore = IOMemory()
        _graph = Graph(rdfstore)
        _graph.load(self.url)
        return _graph


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
