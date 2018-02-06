# -*- coding: utf-8 -*-
"""Harvester Field Config Content Type."""

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from pkan.dcatapde import constants as c
from pkan.dcatapde import _
from pkan.dcatapde.content.fielddefaultfactory import ConfigFieldDefaultFactory
from pkan.dcatapde.vocabularies.dcat_field import DcatFieldVocabulary
from pkan.dcatapde.vocabularies.source_field import SourceFieldVocabulary
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from z3c.relationfield import RelationChoice
from zope import schema
from zope.interface import implementer


class IField(model.Schema):
    """Schema for Harvester Fields."""

    source_field = schema.Choice(
        required=False,
        title=_(u'Source Field'),
        source=SourceFieldVocabulary(),
    )

    prio = schema.Int(
        required=True,
        title=_(u'Priority'),
    )


class ICatalogField(IField):
    dcat_field = schema.Choice(
        required=True,
        title=_(u'Dcat Field'),
        source=DcatFieldVocabulary(c.CT_DCAT_CATALOG),
    )


class IDatasetField(IField):
    dcat_field = schema.Choice(
        required=True,
        title=_(u'Dcat Field'),
        source=DcatFieldVocabulary(c.CT_DCAT_DATASET),
    )


class IDistributionField(IField):
    dcat_field = schema.Choice(
        required=True,
        title=_(u'Dcat Field'),
        source=DcatFieldVocabulary(c.CT_DCAT_DISTRIBUTION),
    )


class ILicenseField(IField):
    dcat_field = schema.Choice(
        required=True,
        title=_(u'Dcat Field'),
        source=DcatFieldVocabulary(c.CT_DCT_LICENSEDOCUMENT),
    )


CT_FIELD_RELATION = {
    c.CT_DCAT_CATALOG: 'catalog_fields',
    c.CT_DCAT_DATASET: 'dataset_fields',
    c.CT_DCAT_DISTRIBUTION: 'distribution_fields',
    c.CT_DCT_LICENSEDOCUMENT: 'license_fields',
}


# fix: because of omitted we need a custom display view
class IHarvesterFieldConfig(model.Schema):
    """Marker interface and DX Python Schema for HarvesterFieldConfig."""

    base_object = RelationChoice(
        required=False,
        title=_(u'Base Object'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(catalog_fields=DataGridFieldFactory)
    form.omitted('catalog_fields')
    catalog_fields = schema.List(
        defaultFactory=ConfigFieldDefaultFactory(c.CT_DCAT_CATALOG),
        description=_(
            u'Select Fields. Required fields can\'t be removed. '
            u'If you remove them, they will be readded after saving.',
        ),
        required=False,
        title=_(u'Catalog Fields'),
        value_type=DictRow(
            title=_(u'Tables'),
            schema=ICatalogField,
        ),
    )

    form.widget(dataset_fields=DataGridFieldFactory)
    form.omitted('dataset_fields')
    dataset_fields = schema.List(
        defaultFactory=ConfigFieldDefaultFactory(c.CT_DCAT_DATASET),
        description=_(
            u'Select Fields. Required fields can\'t be removed. '
            u'If you remove them, they will be readded after saving.',
        ),
        required=False,
        title=_(u'Dataset Fields'),
        value_type=DictRow(
            title=_(u'Tables'),
            schema=IDatasetField,
        ),
    )

    form.widget(distribution_fields=DataGridFieldFactory)
    form.omitted('distribution_fields')
    distribution_fields = schema.List(
        defaultFactory=ConfigFieldDefaultFactory(c.CT_DCAT_DISTRIBUTION),
        description=_(
            u'Select Fields. Required fields can\'t be removed. '
            u'If you remove them, they will be readded after saving.',
        ),
        required=False,
        title=_(u'Distribution Fields'),
        value_type=DictRow(
            title=_(u'Tables'),
            schema=IDistributionField,
        ),
    )

    form.widget(license_fields=DataGridFieldFactory)
    form.omitted('license_fields')
    license_fields = schema.List(
        defaultFactory=ConfigFieldDefaultFactory(c.CT_DCT_LICENSEDOCUMENT),
        description=_(
            u'Select Fields. Required fields can\'t be removed. '
            u'If you remove them, they will be readded after saving.',
        ),
        required=False,
        title=_(u'License Fields'),
        value_type=DictRow(
            title=_(u'Tables'),
            schema=ILicenseField,
        ),
    )


@implementer(IHarvesterFieldConfig)
class HarvesterFieldConfig(Container):
    """Harvester Field Config Content Type."""

    @property
    def fields(self):
        fields = []
        for field in CT_FIELD_RELATION.values():
            fields += getattr(self, field, [])
        return fields


class FieldConfigDefaultFactory(DexterityFactory):
    """Custom DX factory for Harvester Field Config."""

    def __init__(self):
        self.portal_type = c.CT_HARVESTER_FIELD_CONFIG

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.harvester import clean_fieldconfig
        data, errors = clean_fieldconfig(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
