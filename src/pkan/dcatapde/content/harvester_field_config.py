# -*- coding: utf-8 -*-
"""Harvester Field Config Content Type."""

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_HARVESTER_FIELD_CONFIG
from pkan.dcatapde.content.fielddefaultfactory import ConfigFieldDefaultFactory
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from z3c.relationfield import RelationChoice
from zope import schema
from zope.interface import implementer


class IField(model.Schema):
    """Schema for Harvester Fields."""

    dcat_field = schema.Choice(
        required=True,
        title=_(u'Dcat Field'),
        vocabulary='pkan.dcatapde.DcatFieldVocabulary',
    )

    source_field = schema.Choice(
        required=False,
        title=_(u'Source Field'),
        vocabulary='pkan.dcatapde.SourceFieldVocabulary',
    )

    prio = schema.Int(
        required=True,
        title=_(u'Priority'),
    )


class IHarvesterFieldConfig(model.Schema):
    """Marker interface and DX Python Schema for HarvesterFieldConfig."""

    base_object = RelationChoice(
        required=False,
        title=_(u'Base Object'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(fields=DataGridFieldFactory)
    fields = schema.List(
        defaultFactory=ConfigFieldDefaultFactory,
        description=_(
            u'Select Fields. Required fields can\'t be removed. '
            u'If you remove them, they will be readded after saving.',
        ),
        required=True,
        title=_(u'Fields'),
        value_type=DictRow(
            title=_(u'Tables'),
            schema=IField,
        ),
    )


@implementer(IHarvesterFieldConfig)
class HarvesterFieldConfig(Container):
    """Harvester Field Config Content Type."""


class FieldConfigDefaultFactory(DexterityFactory):
    """Custom DX factory for Harvester Field Config."""

    def __init__(self):
        self.portal_type = CT_HARVESTER_FIELD_CONFIG

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.harvester import clean_fieldconfig
        data, errors = clean_fieldconfig(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
