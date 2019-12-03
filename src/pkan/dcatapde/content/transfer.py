# -*- coding: utf-8 -*-
"""Transfer Content Type."""
from pkan.dcatapde import _
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.i18n import HELP_REHARVESTING_PERIOD
from plone.dexterity.content import Container
from plone.supermodel import model
from pytimeparse import parse
from re import fullmatch
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant

import zope.schema as schema


TARGET_NAMESPACE_REGEX = r'[a-zA-Z0-9_\-]*'


def period_constraint(value):
    res = parse(value)
    if not res:
        raise Invalid(_(u'Expression can not be parsed.'))
    return True


def target_namespace_constraint(value):
    res = fullmatch(TARGET_NAMESPACE_REGEX, value)
    return res


class ITransfer(model.Schema):
    """Marker interfce and Dexterity Python Schema for Transfer."""

    url = schema.URI(
        required=False,
        title=_(u'Harvesting Source'),
        description=_(u'The URI of the source of data to be harvested.'),
    )

    source_type = schema.Choice(
        required=False,
        title=_(u'Source Format'),
        description=_(
            u'Transport format of the source. Usually this will be a RDF '
            u'variant like (JSON-LD, XML, Turtle), or a generic '
            u'source like "JSON generic"',
        ),
        vocabulary='pkan.dcatapde.RdfTypeVocabulary',
    )

    source_namespace = schema.TextLine(
        title=_(u'Source Namespace'),
        description=_(
            u'Specify a name for the tripelstore to harvest to. '
            u'Only a single word without blanks allowed',
        ),
        constraint=target_namespace_constraint,
        required=False,
    )

    target_namespace = schema.TextLine(
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

    @invariant
    def validateSource(data):
        if data.url is not None and data.source_type is not None:
            return
        elif data.source_namespace is not None:
            return
        raise Invalid(
            _('You need a url with source_type or an namespace as source'),
        )


@implementer(ITransfer)
class Transfer(Container, DCATMixin):
    """Transfer Content Type."""

    def __init__(self, *args, **kwargs):

        self._graph = None
        self._rdfstore = None

        super(Transfer, self).__init__(*args, **kwargs)

    def id_in_tripel_store(self):
        """This has to be improved"""
        if self.target_namespace:
            return self.target_namespace
        return self.UID()
