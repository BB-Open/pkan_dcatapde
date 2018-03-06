# -*- coding: utf-8 -*-
"""Harvester Content Type."""
from pkan.dcatapde import _
from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.constants import CT_HARVESTER
from pkan.dcatapde.constants import DCAT_TOP_NODES
from pkan.dcatapde.structure.sparql import QUERY_A
from pkan.widgets.ajaxselect import AjaxSelectAddFieldWidget
from pkan.widgets.query.widget import QueryWidget
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from zope.interface import implementer
from zope.schema.vocabulary import SimpleVocabulary

import json
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

    top_node = schema.Choice(
        required=True,
        title=_(u'Portal Type of Top Node'),
        vocabulary=SimpleVocabulary.fromValues(DCAT_TOP_NODES),
    )

    form.widget(
        'top_node_sparql',
        QueryWidget,
    )
    top_node_sparql = schema.Text(
        required=True,
        title=_(u'Query'),
        default=u'Hello World',
    )

    preview = schema.Text(
        required=False,
        title=_(u'Preview'),
        description=_(u'Preview of the Sparqle Query'),
        default=_('No value'),
    )


@implementer(IHarvester)
class Harvester(Container):
    """Harvester Content Type."""

    def __init__(self, *args, **kwargs):

        self._graph = None
        self._rdfstore = None

        super(Harvester, self).__init__(*args, **kwargs)

    @property
    def mapper(self):
        """Dummy mapper since Entity Mapper is working"""
        result = {}
        result['dcat:Catalog'] = QUERY_A
        result['dcat:Dataset'] = QUERY_A
        result['dcat:Distribution'] = QUERY_A
        return result

    def get_preview(self):
        processor = self.source_type(self)
        preview = processor.get_preview()
        pretty = json.dumps(preview)
        self.request.response.setHeader('Content-type', 'application/json')
        return pretty


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
