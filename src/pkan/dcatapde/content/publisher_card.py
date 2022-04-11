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

    form.widget(
        'dct_publisher',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_FOAF_AGENT,
        content_type_title=i18n.LABEL_DCT_PUBLISHER,
        initial_path='/publishers/',
    )
    dct_publisher = schema.Choice(
        description=i18n.HELP_DCT_PUBLISHER,
        required=False,
        title=i18n.LABEL_DCT_PUBLISHER,
        vocabulary='pkan.dcatapde.vocabularies.FOAFAgent',
    )

    read_permission(foaf_name_input='cmf.ManagePortal')
    write_permission(foaf_name_input='cmf.ManagePortal')
    foaf_name_input = schema.TextLine(
        required=False,
        title=_(u'foaf:Name for Publisher'),
        description=_(u'The foaf:Name of the Sparql-Object to be linked if no publisher is selected.'),
    )

    foaf_name = schema.TextLine(
        title=_(u'SPARQL Identifier for Publisher'),
        description=_(u'The URI of the Sparql-Object to be linked.'),
        readonly=True
    )


def publisher_card_modified(obj, event):
    if obj.dct_publisher:
        pub_obj = api.content.get(UID=obj.dct_publisher)
        if pub_obj.foaf_name:
            if 'deu' in pub_obj.foaf_name:
                obj.foaf_name = pub_obj.foaf_name['deu']
            elif 'eng' in pub_obj.foaf_name:
                obj.foaf_name = pub_obj.foaf_name['eng']
            else:
                lang = list(pub_obj.foaf_name)[0]
                obj.foaf_name = pub_obj.foaf_name[lang]
        elif pub_obj.rdfs_isDefinedBy:
            obj.foaf_name = pub_obj.rdfs_isDefinedBy
        else:
            obj.foaf_name = pub_obj.dct_identifier
    else:
        obj.foaf_name = obj.foaf_name_input
