# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from pkan.dcatapde import _
from pkan.dcatapde.api.harvester import add_harvester_field_config
from pkan.dcatapde.constants import CT_HarvesterFieldConfig
from pkan.dcatapde.content.fielddefaultfactories import ConfigFieldDefaultFactory
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IField(model.Schema):

    dcat_field = schema.Choice(
        vocabulary='pkan.dcatapde.DcatFieldVocabulary',
        title=_(u'Dcat Field'),
        required=True,
    )

    source_field = schema.Choice(
        vocabulary='pkan.dcatapde.SourceFieldVocabulary',
        title=_(u'Source Field'),
        required=False,
    )


class IHarvesterFieldConfig(model.Schema):
    ''' Marker interface and Dexterity Python Schema for HarvesterFieldConfig
    '''

    form.widget(fields=DataGridFieldFactory)
    fields = schema.List(
        title=_(u'Fields'),
        description=_(
            u'''Select Fields. Required fields can't be removed.
            If you remove them, they will be readded after saving.'''),
        defaultFactory=ConfigFieldDefaultFactory,
        value_type=DictRow(
            title=_(u'Tables'),
            schema=IField,
        ),
        required=True,
    )


@implementer(IHarvesterFieldConfig)
class HarvesterFieldConfig(Container):
    '''
    '''


class FieldConfigDefaultFactory(DexterityFactory):

    def __init__(self):
        self.portal_type = CT_HarvesterFieldConfig

    def __call__(self, *args, **kw):
        # TODO: get context and maybe change it
        data = add_harvester_field_config(None, dry_run=True, **kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
