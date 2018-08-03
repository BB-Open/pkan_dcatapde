# -*- coding: utf-8 -*-
"""Harvester Content Type."""
from pkan.dcatapde import _
from pkan.dcatapde import i18n
from pkan.dcatapde.constants import DCAT_TOP_NODES
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.i18n import HELP_REHARVESTING_PERIOD
from pkan.dcatapde.structure.sparql import QUERY_A
from pkan.dcatapde.structure.sparql import QUERY_A_STR
from pkan.widgets.ajaxselect import AjaxSelectAddFieldWidget
from pkan.widgets.sparqlquery import SparqlQueryFieldWidget
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.supermodel import model
from pytimeparse import parse
from z3c.form.interfaces import IEditForm
from zope.interface import implementer
from zope.interface import Invalid
from zope.schema.vocabulary import SimpleVocabulary

import zope.schema as schema


def period_constraint(value):
    res = parse(value)
    if not res:
        raise Invalid(_(u'Expression can not be parsed.'))
    return True


class IHarvester(model.Schema):
    """Marker interfce and Dexterity Python Schema for Harvester."""

    url = schema.URI(
        required=True,
        title=_(u'Harvesting Source'),
        description=_(u'The URI of the source of data to be harvested.'),
    )

    form.omitted('base_object')
    form.no_omit(IEditForm, 'base_object')
    form.widget(
        'base_object',
        AjaxSelectAddFieldWidget,
    )
    base_object = schema.Choice(
        required=False,
        title=i18n.LABEL_BASE_OBJECT,
        vocabulary='pkan.dcatapde.vocabularies.ContextAwareDCATCatalog',
        description=i18n.HELP_BASE_OBJECT,
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

    # Todo: use in harvesting process
    new_workflow_state = schema.Choice(
        required=False,
        title=_(u'Workflow State of created objects'),
        vocabulary='pkan.dcatapde.WorkflowStates',
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
