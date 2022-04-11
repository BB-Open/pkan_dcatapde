# -*- coding: utf-8 -*-
"""PublisherCard Content Type."""
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

    foaf_name = schema.TextLine(
        title=_(u'foaf:name for Publisher'),
        description=_(
            u'The name must be identical to the name used in the faceted search (frontend). It is used to generate the short cut to the search results of the publisher. If the value differs from the foaf:name used in the data, no search results can be found.'),
        readonly=False
    )
