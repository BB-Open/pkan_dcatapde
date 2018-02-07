# -*- coding: utf-8 -*-
"""DCATCatalog Content Type."""

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from pkan.widgets.relateditems import RelatedItemsFieldWidget
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from z3c.relationfield import RelationChoice
from zope.interface import implementer

import zope.schema as schema


class IDCATCatalog(model.Schema):
    """Marker interface and Dexterity Python Schema for DCATCatalog."""

    # Fieldsets
    # -------------------------------------------------------------------------
    model.fieldset(
        'linking',
        label=i18n.FIELDSET_RELATIONS,
        fields=[
            'dct_hasPart',
            'dct_isPartOf',
            'dct_spatial',
        ],
    )

    # Mandatory
    # -------------------------------------------------------------------------
    dct_title = I18NTextLine(
        required=True,
        title=i18n.LABEL_DCT_TITLE,
    )

    dct_description = I18NText(
        required=True,
        title=i18n.LABEL_DCT_DESCRIPTION,
    )

    form.widget(
        'dct_publisher',
        RelatedItemsFieldWidget,
        content_type=constants.CT_FOAF_AGENT,
        content_type_title=i18n.LABEL_DCT_PUBLISHER,
        initial_path='/publisher/',
        pattern_options={
            'selectableTypes': [constants.CT_FOAF_AGENT],
        },
    )
    dct_publisher = RelationChoice(
        description=i18n.HELP_DCT_PUBLISHER,
        required=True,
        title=i18n.LABEL_DCT_PUBLISHER,
        vocabulary='plone.app.vocabularies.Catalog',
    )

    # Recommended
    # -------------------------------------------------------------------------
    form.widget(
        'dct_license',
        RelatedItemsFieldWidget,
        content_type=constants.CT_DCT_LICENSEDOCUMENT,
        content_type_title=i18n.LABEL_DCT_LICENSE,
        initial_path='/licenses/',
        pattern_options={
            'selectableTypes': [constants.CT_DCT_LICENSEDOCUMENT],
        },
    )
    dct_license = RelationChoice(
        description=i18n.HELP_DCT_LICENSE,
        required=False,
        title=i18n.LABEL_DCT_LICENSE,
        vocabulary='plone.app.vocabularies.Catalog',
    )

    foaf_homepage = schema.URI(
        required=False,
        title=i18n.LABEL_FOAF_HOMEPAGE,
    )

    form.widget(
        'dct_language',
        AjaxSelectFieldWidget,
        vocabulary='plone.app.vocabularies.AvailableContentLanguages',
    )
    dct_language = schema.List(
        required=False,
        title=i18n.LABEL_DCT_LANGUAGE,
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.AvailableContentLanguages',
        ),
    )

    form.widget(
        'dcat_themeTaxonomy',
        RelatedItemsFieldWidget,
        content_type=constants.CT_DCT_LICENSEDOCUMENT,
        content_type_title=i18n.LABEL_DCT_THEMETAXONOMY,
        initial_path='/licenses/',
        pattern_options={
            'selectableTypes': [constants.CT_DCT_LICENSEDOCUMENT],
        },
    )
    dcat_themeTaxonomy = RelationChoice(
        description=i18n.HELP_DCT_THEMETAXONOMY,
        required=False,
        title=i18n.LABEL_DCT_THEMETAXONOMY,
        vocabulary='plone.app.vocabularies.Catalog',
    )

    # Optional
    # -------------------------------------------------------------------------
    form.widget(
        'dct_rights',
        RelatedItemsFieldWidget,
        content_type=constants.CT_DCT_LICENSEDOCUMENT,
        content_type_title=i18n.LABEL_DCT_RIGHTS,
        initial_path='/licenses/',
        pattern_options={
            'selectableTypes': [constants.CT_DCT_LICENSEDOCUMENT],
        },
    )
    dct_rights = RelationChoice(
        description=i18n.HELP_DCT_RIGHTS,
        required=False,
        title=i18n.LABEL_DCT_RIGHTS,
        vocabulary='plone.app.vocabularies.Catalog',
    )

    dct_issued = schema.Date(
        required=False,
        title=i18n.LABEL_DCT_ISSUED,
    )

    dct_modified = schema.Date(
        required=False,
        title=i18n.LABEL_DCT_MODIFIED,
    )

    form.widget(
        'dct_hasPart',
        RelatedItemsFieldWidget,
        content_type=constants.CT_DCAT_CATALOG,
        content_type_title=i18n.LABEL_DCT_HASPART,
        initial_path='/',
        pattern_options={
            'selectableTypes': [constants.CT_DCAT_CATALOG],
        },
    )
    dct_hasPart = RelationChoice(
        description=i18n.HELP_DCT_HASPART,
        required=False,
        title=i18n.LABEL_DCT_HASPART,
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(
        'dct_isPartOf',
        RelatedItemsFieldWidget,
        content_type=constants.CT_DCAT_CATALOG,
        content_type_title=i18n.LABEL_DCT_ISPARTOF,
        initial_path='/',
        pattern_options={
            'selectableTypes': [constants.CT_DCAT_CATALOG],
        },
    )
    dct_isPartOf = RelationChoice(
        description=i18n.HELP_DCT_ISPARTOF,
        required=False,
        title=i18n.LABEL_DCT_ISPARTOF,
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(
        'dct_spatial',
        RelatedItemsFieldWidget,
        content_type=constants.CT_DCT_LOCATION,
        content_type_title=i18n.LABEL_DCT_SPATIAL,
        initial_path='/locations/',
        pattern_options={
            'selectableTypes': [constants.CT_DCT_LOCATION],
        },
    )
    dct_spatial = RelationChoice(
        description=i18n.HELP_DCT_SPATIAL,
        required=False,
        title=i18n.LABEL_DCT_SPATIAL,
        vocabulary='plone.app.vocabularies.Catalog',
    )


@implementer(IDCATCatalog)
class DCATCatalog(Container, DCATMixin):
    """DCATCatalog Content Type."""

    _namespace = 'dcat'
    _ns_class = 'catalog'

    dct_title = I18NTextProperty(IDCATCatalog['dct_title'])
    dct_description = I18NTextProperty(IDCATCatalog['dct_description'])

    def Title(self):
        return unicode(self.dct_title)

    def Description(self):
        return self.dct_description


class DCATCatalogDefaultFactory(DexterityFactory):
    """Custom DX factory for DCATCatalog."""

    def __init__(self):
        self.portal_type = constants.CT_DCAT_CATALOG

    def __call__(self, *args, **kw):
        from pkan.dcatapde.api.catalog import clean_catalog

        data, errors = clean_catalog(**kw)

        return super(
            DCATCatalogDefaultFactory,
            self,
        ).__call__(*args, **data)
