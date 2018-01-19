# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from pkan.dcatapde import _
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import provider
from zope.schema._bootstrapinterfaces import IContextAwareDefaultFactory
from zope.schema.interfaces import IVocabularyFactory


@provider(IContextAwareDefaultFactory)
def FieldDefaultFactory(context):
        fields = []

        vocab_name = 'pkan.dcatapde.DcatFieldVocabulary'
        factory = getUtility(IVocabularyFactory, vocab_name)
        options = factory(context)

        for value in options.by_value.keys():
            if 'required' in value:
                fields.append(
                    {
                        'dcat_field': value,
                        'source_field': None
                    }
                )

        return fields


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
        defaultFactory=FieldDefaultFactory,
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
