# -*- coding: utf-8 -*-
"""Harvester Content Type."""
from pkan.dcatapde import _
from pkan.dcatapde.api.functions import query_published_objects_in_context
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
from pkan.widgets.ajaxselect.widget import AjaxSelectAddFieldWidget
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.autoform import directives as form
from plone.autoform.directives import read_permission, write_permission
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope.interface.declarations import implementer
from plone.dexterity.content import Container, Item
from plone import api
from pkan.dcatapde import _, constants, i18n

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


class ILGBHarvester(model.Schema):
    """Marker interfce and Dexterity Python Schema for Harvester."""

    csw_url = schema.URI(
        required=True,
        title=_(u'CSW URL'),
        description=_(u'The URI of the csw data to be harvested.'),
    )

    csw_output_schema = schema.URI(
        required=True,
        title=_(u'CSW OUTPUT SCHEMA'),
        description=_(u'The URI of the output Scheme.'),
    )

    dcm_url = schema.URI(
        required=False,
        title=_(u'DCM Source'),
        description=_(u'The URI of the dcm data to be harvested. DCM provides information about publishers, catalogs and priority. If not provided, Fallback-URL and Fallback-Name will be used.'),
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

    fallback_url = schema.URI(
        required=True,
        title=_(u'Fallback-Url'),
        description=_(u'The base uri used for missing Information in DCM.'),
    )

    fallback_name = schema.TextLine(
        required=True,
        title=_('Fallback-Name'),
        description=_(u'Title of generated Fallback-Catalog and Fallback-Publisher for missinf Information in DCM')
    )


@implementer(ILGBHarvester)
class LGBHarvester(Container, DCATMixin):
    """Harvester Content Type."""

    def __init__(self, *args, **kwargs):

        self._graph = None
        self._rdfstore = None

        super(LGBHarvester, self).__init__(*args, **kwargs)

    @property
    def id_in_tripel_store(self):
        """This has to be improved"""
        if self.target_namespace:
            return self.target_namespace
        return self.UID()

    @property
    def target(self):
        return HARVEST_TRIPELSTORE

    @property
    def config(self):
        return 'lgb.yaml'
