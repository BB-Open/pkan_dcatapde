# -*- coding: utf-8 -*-
"""Catalog Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.constants import CT_FOAF_AGENT
from pkan.dcatapde.content.base import DCATMixin
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.formwidget.relateditems import RelatedItemsFieldWidget
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from z3c.relationfield import RelationChoice
from zope.interface import implementer

import zope.schema as schema


class IDCATCatalog(model.Schema):
    """Marker interfce and Dexterity Python Schema for Catalog."""

    # Mandatory
    # ------------------------------
    dct_title = I18NTextLine(
        required=True,
        title=_(u'Title'),
    )

    dct_description = I18NText(
        required=True,
        title=_(u'Description'),
    )

    form.widget(
        'dct_publisher',
        RelatedItemsFieldWidget,
        content_type=CT_FOAF_AGENT,
        content_type_title=_(u'Publisher'),
        initial_path='/publisher/',
        pattern_options={
            'selectableTypes': [CT_FOAF_AGENT],
        },
    )

    dct_publisher = RelationChoice(
        description=_(
            u'Add a new publisher or chose one from the list of publishers',
        ),
        required=True,
        title=_(u'Publisher'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    # Recommended
    # ------------------------------
    form.widget(
        'dct_license',
        RelatedItemsFieldWidget,
        content_type=CT_DCT_LICENSEDOCUMENT,
        content_type_title=_(u'License'),
        initial_path='/licenses/',
        pattern_options={
            'selectableTypes': [CT_DCT_LICENSEDOCUMENT],
        },
    )

    dct_license = RelationChoice(
        description=_(
            u'Add a new license or chose one from the list of licenses',
        ),
        required=False,
        title=_(u'License'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    foaf_homepage = schema.URI(
        required=False,
        title=(u'Homepage'),
    )

    form.widget(
        'dct_language',
        AjaxSelectFieldWidget,
        vocabulary='plone.app.vocabularies.AvailableContentLanguages',
    )

    dct_language = schema.List(
        title=_(u'Languages'),
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.AvailableContentLanguages',
        ),
        required=False,
    )

    form.widget(
        'dcat_themeTaxonomy',
        RelatedItemsFieldWidget,
        content_type='dct_licensedocument',
        content_type_title=_(u'Theme Taxonomy'),
        initial_path='/licenses/',
        pattern_options={
            'selectableTypes': ['dct_licensedocument'],
        },
    )

    dcat_themeTaxonomy = RelationChoice(
        description=_(
            u'Add a new Theme Taxonomy or chose one from the list',
        ),
        required=False,
        title=_(u'Theme Taxonomy'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    # Optional
    # -----------------------------------------------------

    form.widget(
        'dct_rights',
        RelatedItemsFieldWidget,
        content_type='dct_licensedocument',
        content_type_title=_(u'Rights'),
        initial_path='/licenses/',
        pattern_options={
            'selectableTypes': ['dct_licensedocument'],
        },
    )

    dct_rights = RelationChoice(
        description=_(
            u'Add a new rights statement or chose one from the list of '
            u'statements',
        ),
        required=False,
        title=_(u'Rights'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    dct_issued = schema.Date(
        required=False,
        title=(u'Issued'),
    )

    dct_modified = schema.Date(
        required=False,
        title=(u'Modified'),
    )

    model.fieldset(
        'linking',
        label=_(u'Relations'),
        fields=[
            'dct_hasPart',
            'dct_isPartOf',
            'dct_spatial',
        ],
    )

    form.widget(
        'dct_hasPart',
        RelatedItemsFieldWidget,
        content_type='catalog',
        content_type_title=_(u'Parts'),
        initial_path='/',
        pattern_options={
            'selectableTypes': ['catalog'],
        },
    )

    dct_hasPart = RelationChoice(
        title=_(u'Parts'),
        description=_(
            u'Add a new Catalog or link to an existing',
        ),
        required=False,
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(
        'dct_isPartOf',
        RelatedItemsFieldWidget,
        content_type='catalog',
        content_type_title=_(u'Parent Catalog'),
        initial_path='/',
        pattern_options={
            'selectableTypes': ['catalog'],
        },
    )

    dct_isPartOf = RelationChoice(
        description=_(
            u'Add a new Parent Catalog or link to an existing',
        ),
        required=False,
        title=_(u'Parent Catalog'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(
        'dct_spatial',
        RelatedItemsFieldWidget,
        content_type='dct_location',
        content_type_title=_(u'Spatial relevance'),
        initial_path='/locations/',
        pattern_options={
            'selectableTypes': ['dct_location'],
        },
    )

    dct_spatial = RelationChoice(
        description=_(
            u'Add a new Location or link to an existing',
        ),
        required=False,
        title=_(u'Spatial relevance'),
        vocabulary='plone.app.vocabularies.Catalog',
    )


@implementer(IDCATCatalog)
class DCATCatalog(Container, DCATMixin):
    """Catalog Content Type."""

    _namespace = 'dcat'
    _ns_class = 'catalog'


class DCATCatalogDefaultFactory(DexterityFactory):
    """Custom DX factory for Catalog."""

    def __init__(self):
        self.portal_type = CT_DCAT_CATALOG

    def __call__(self, *args, **kw):
        from pkan.dcatapde.api.catalog import clean_catalog

        data, errors = clean_catalog(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
