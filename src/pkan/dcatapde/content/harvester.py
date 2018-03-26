# -*- coding: utf-8 -*-
"""Harvester Content Type."""
from pkan.dcatapde import _
from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.constants import CT_HARVESTER
from pkan.dcatapde.constants import DCAT_TOP_NODES
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.structure.sparql import QUERY_A
from pkan.dcatapde.structure.sparql import QUERY_A_STR
from pkan.widgets.ajaxselect import AjaxSelectAddFieldWidget
from pkan.widgets.sparqlquery import SparqlQueryFieldWidget
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from zope.interface import implementer
from zope.schema.vocabulary import SimpleVocabulary

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
        vocabulary='pkan.dcatapde.vocabularies.PortalCatalog',
        description=i18n.HELP_BASE_OBJECT,
    )

    # harvesting_type = schema.Choice(
    #     # Todo: reset to true when new adapter are added
    #     required=False,
    #     title=_(u'Harvesting target'),
    #     description=_(
    #         u'The Harvesting target chooses the output processor for the '
    #         u'harvested data.Here one can chose if the imported triples were'
    #         u' added to common catalogs section (default), or if the '
    #         u'harvested data is a controlled vacabulary e.g. Licenses from '
    #         u'dcat-ap.de that should be imported into the licenses folder'
    #         u'Not yet implemented! Choose "default"!',
    #     ),
    #     vocabulary='pkan.dcatapde.HarvestingVocabulary',
    # )

    # data_cleaner = schema.Choice(
    #     required=True,
    #     title=_(u'Processor/Filter'),
    #     description=_(
    #         u'The processor depends on the sematic of the data and may be '
    #         u'specific to a certain data provider or data format e.g. OGD.'
    #         u'Currently only "PotsdamCleaner" is available.',
    #     ),
    #     vocabulary='pkan.dcatapde.DataCleanerVocabulary',
    # )

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

    top_node = schema.Choice(
        required=True,
        title=_(u'Portal Type of Top Node'),
        vocabulary=SimpleVocabulary.fromValues(DCAT_TOP_NODES),
    )

    form.widget(
        'top_node_sparql',
        SparqlQueryFieldWidget,
    )
    top_node_sparql = schema.Text(
        required=True,
        title=_(u'Query'),
        default=QUERY_A_STR,
    )


@implementer(IHarvester)
class Harvester(Container, DCATMixin):
    """Harvester Content Type."""

    def __init__(self, *args, **kwargs):

        self._graph = None
        self._rdfstore = None

        super(Harvester, self).__init__(*args, **kwargs)

    @property
    def mapper(self):
        """Dummy mapper since Entity Mapper is working"""
        # todo: Update results with values from config stored in annotations
        # annotations = IAnnotations(self)
        # if HARVESTER_ENTITY_KEY in annotations:
        #     sparql = annotations[HARVESTER_ENTITY_KEY]
        # else:
        #     sparql = {}
        # if HARVESTER_DEXTERITY_KEY in annotations:
        #     dexterity = annotations[HARVESTER_DEXTERITY_KEY]
        # else:
        #     dexterity = {}
        # if HARVESTER_DEFAULT_KEY in annotations:
        #     str_defaults = annotations[HARVESTER_DEFAULT_KEY]
        # else:
        #     str_defaults = {}

        result = {}

        # todo: read this from harvester directly
        result['dcat:Catalog'] = QUERY_A
        result['dcat:Dataset'] = QUERY_A
        result['dcat:Distribution'] = QUERY_A
        return result


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
