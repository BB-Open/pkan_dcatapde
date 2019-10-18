# -*- coding: utf-8 -*-
"""PublisherCard Content Type."""

import zope.schema as schema
from pkan.dcatapde import _
from pkan.dcatapde import constants
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope.interface import implementer
from plone.autoform import directives as form
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget


class IPublisherCard(model.Schema):
    """Marker interface and Dexterity Python Schema for PublisherCard."""

    title = schema.TextLine(
        required=True,
        title=_(u'Publisher Name'),
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    logo = NamedBlobImage(
        title=_(u'Logo'),
        required=False,
    )

    form.widget('text', WysiwygFieldWidget)
    text = schema.Text(
        title=_('Text'),
        required=False,
    )

    sparql_identifier = schema.URI(
        required=False,
        title=_(u'SPARQL Identifier for Publisher'),
        description=_(u'The URI of the Sparql-Object to be linked.'),
    )
