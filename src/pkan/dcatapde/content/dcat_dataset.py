# -*- coding: utf-8 -*-
"""Dataset Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.content.base import DCATMixin
from pkan.widgets import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from z3c.relationfield import RelationChoice
from zope.interface import implementer

import zope.schema as schema


class IDCATDataset(model.Schema):
    """Marker interfce and Dexterity Python Schema for Dataset."""

    dct_title = I18NTextLine(
        required=True,
        title=_(u'Title'),
    )

    dct_description = I18NText(
        required=True,
        title=_(u'Description'),
    )

    dcatde_contributorID = I18NTextLine(
        required=True,
        title=_(u'Contributor ID'),
    )

    rdf_about = schema.URI(
        required=True,
        title=_(u'Access URI'),
    )

    model.fieldset(
        'agents',
        label=_(u'Agents'),
        fields=[
            'dct_publisher',
            'dct_creator',
            'dct_contributor',
            'dcatde_originator',
            'dcatde_maintainer',
        ],
    )

    form.widget(
        'dct_publisher',
        RelatedItemsFieldWidget,
        content_type='foafagent',
        content_type_title=_(u'Publisher'),
        initial_path='/publisher/',
        pattern_options={
            'selectableTypes': ['foafagent'],
        },
    )

    dct_publisher = RelationChoice(
        description=_(
            u'Add a new publisher or chose one from the list of publishers',
        ),
        required=False,
        title=_(u'Publisher'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(
        'dct_creator',
        RelatedItemsFieldWidget,
        content_type='foafagent',
        content_type_title=_(u'Creator'),
        initial_path='/agents/',
        pattern_options={
            'selectableTypes': ['foafagent'],
        },
    )

    dct_creator = RelationChoice(
        required=False,
        title=_(u'Creator'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(
        'dct_contributor',
        RelatedItemsFieldWidget,
        content_type='foafagent',
        content_type_title=_(u'Contributor'),
        initial_path='/agents/',
        pattern_options={
            'selectableTypes': ['foafagent'],
        },
    )

    dct_contributor = RelationChoice(
        required=False,
        title=_(u'Contributor'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(
        'dcatde_originator',
        RelatedItemsFieldWidget,
        content_type='foafagent',
        content_type_title=_(u'Originator'),
        initial_path='/agents/',
        pattern_options={
            'selectableTypes': ['foafagent'],
        },
    )

    dcatde_originator = RelationChoice(
        required=False,
        title=_(u'Originator'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(
        'dcatde_maintainer',
        RelatedItemsFieldWidget,
        content_type='foafagent',
        content_type_title=_(u'Maintainer'),
        initial_path='/agents/',
        pattern_options={
            'selectableTypes': ['foafagent'],
        },
    )

    dcatde_maintainer = RelationChoice(
        required=False,
        title=_(u'Maintainer'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    model.fieldset(
        'details',
        label=_(u'Dates, Geo, etc'),
        fields=[
            'dct_issued',
            'dct_modified',
            'dcatde_politicalGeocodingURI',
            'dcatde_politicalGeocodingLevelURI',
            'dct_identifier',
            'owl_versionInfo',
            'dcatde_legalbasisText',
            'adms_versionNotes',
            'foaf_landingpage',
            'foaf_page',

        ],
    )

    dct_issued = schema.Date(
        required=False,
        title=(u'Issued'),
    )

    dct_modified = schema.Date(
        required=False,
        title=(u'Modified'),
    )
    dcatde_geocodingText = I18NTextLine(
        required=False,
        title=_(u'Geocoding text'),
    )

    dcatde_politicalGeocodingURI = schema.URI(
        required=False,
        title=_(u'PoliticalGeocodingURI'),
    )

    dcatde_politicalGeocodingLevelURI = schema.URI(
        required=False,
        title=_(u'PoliticalGeocodingLevelURI'),
    )

    dct_identifier = I18NTextLine(
        required=False,
        title=_(u'Identifier'),
    )

    owl_versionInfo = I18NTextLine(
        required=False,
        title=_(u'Version info'),
    )
    dcatde_legalbasisText = I18NTextLine(
        required=False,
        title=_(u'Legal basis text'),
    )
    adms_versionNotes = I18NTextLine(
        required=False,
        title=_(u'Version Notes'),
    )

    foaf_landingpage = schema.URI(
        required=False,
        title=_(u'Landing page'),
    )

    foaf_page = schema.URI(
        required=False,
        title=_(u'Page'),
    )


@implementer(IDCATDataset)
class DCATDataset(Container, DCATMixin):
    """Dataset Content Type."""

    _namespace = 'dcat'
    _ns_class = 'dataset'


class DCATDatasetDefaultFactory(DexterityFactory):
    """Custom DX factory for Dataset."""

    def __init__(self):
        self.portal_type = CT_DCAT_DATASET

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.dataset import clean_dataset
        data, errors = clean_dataset(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
