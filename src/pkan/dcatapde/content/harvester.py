# -*- coding: utf-8 -*-
"""Harvester Content Type."""
from pkan.dcatapde import _
from pkan.dcatapde.api.functions import query_active_objects_in_context
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import CT_DCAT_COLLECTION_CATALOG
from pkan.dcatapde.constants import HARVEST_TRIPELSTORE
from pkan.dcatapde.constants import RDF_FORMAT_JSONLD
from pkan.dcatapde.constants import RDF_FORMAT_METADATA
from pkan.dcatapde.constants import RDF_FORMAT_TURTLE
from pkan.dcatapde.constants import RDF_FORMAT_XML
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.harvesting.manager.interfaces import IRDFJSONLD
from pkan.dcatapde.harvesting.manager.interfaces import IRDFTTL
from pkan.dcatapde.harvesting.manager.interfaces import IRDFXML
from pkan.dcatapde.i18n import HELP_REHARVESTING_PERIOD
from pkan.dcatapde.structure.sparql import QUERY_A
from pkan.dcatapde.structure.sparql import QUERY_A_STR
from plone.dexterity.content import Container
from plone.supermodel import model
from pytimeparse import parse
from re import fullmatch
from zope.interface import implementer
from zope.interface import Invalid

import zope.schema as schema


TARGET_NAMESPACE_REGEX = r'[a-zA-Z0-9_\-]*'

INTERFACE_FORMAT = {
    IRDFJSONLD: RDF_FORMAT_JSONLD,
    IRDFXML: RDF_FORMAT_XML,
    IRDFTTL: RDF_FORMAT_TURTLE,
}

INTERFACE_VIEW = {
    IRDFJSONLD: '/rdf_json',
    IRDFXML: '/rdf_xml',
    IRDFTTL: '/rdf_ttl',
}


def period_constraint(value):
    res = parse(value)
    if not res:
        raise Invalid(_(u'Expression can not be parsed.'))
    return True


def target_namespace_constraint(value):
    res = fullmatch(TARGET_NAMESPACE_REGEX, value)
    return res


class IHarvester(model.Schema):
    """Marker interfce and Dexterity Python Schema for Harvester."""

    url = schema.URI(
        required=False,
        title=_(u'Harvesting Source'),
        description=_(u'The URI of the source of data to be harvested.'),
    )

    source_type = schema.Choice(
        required=True,
        title=_(u'Source Format'),
        description=_(
            u'Transport format of the source. Usually this will be a RDF '
            u'variant like (JSON-LD, XML, Turtle), or a generic '
            u'source like "JSON generic"',
        ),
        vocabulary='pkan.dcatapde.RdfTypeVocabulary',
    )

    target_namespace = schema.TextLine(
        required=True,
        title=_(u'Target Namespace'),
        description=_(
            u'Specify a name for the tripelstore to harvest to. '
            u'Only a single word without blanks allowed',
        ),
        constraint=target_namespace_constraint,
    )

    reharvesting_period = schema.TextLine(
        required=False,
        title=_(u'Reharvesting Period'),
        description=_(HELP_REHARVESTING_PERIOD),
        constraint=period_constraint,
    )

    last_run = schema.Datetime(
        required=False,
        title=_(u'Last Run'),
        readonly=True,
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

    @property
    def id_in_tripel_store(self):
        """This has to be improved"""
        if self.target_namespace:
            return self.target_namespace
        return self.UID()

    @property
    def mime_type(self):
        format_interface = self.source_type
        format_type = INTERFACE_FORMAT[format_interface]
        mimetype = RDF_FORMAT_METADATA[format_type]['mime_type']
        return mimetype

    @property
    def serialize_format(self):
        format_interface = self.source_type
        format_type = INTERFACE_FORMAT[format_interface]
        mimetype = RDF_FORMAT_METADATA[format_type]['serialize_as']
        return mimetype

    @property
    def target(self):
        return HARVEST_TRIPELSTORE

    @property
    def top_node(self):
        return CT_DCAT_CATALOG

    @property
    def top_node_sparql(self):
        return QUERY_A_STR

    @property
    def rdf_view(self):
        return INTERFACE_VIEW[self.source_type]

    @property
    def catalog_urls(self):
        view = self.rdf_view
        urls = []
        catalogs = query_active_objects_in_context({}, CT_DCAT_CATALOG, context=self)
        for catalog in catalogs:
            url = catalog.absolute_url() + view
            urls.append(url)
        collections = query_active_objects_in_context({}, CT_DCAT_COLLECTION_CATALOG, context=self)
        for catalog in collections:
            url = catalog.absolute_url() + view
            urls.append(url)
        return urls
