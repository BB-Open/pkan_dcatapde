# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.constants import HARVESTER_ENTITY_KEY
from pkan.dcatapde.structure.sparql import QUERY_ATT_STR
from pkan.dcatapde.vocabularies.dcat_field import DcatFieldVocabulary
from pkan.widgets.sparqlquery import SparqlQueryFieldWidget
from plone.autoform import directives as form
from plone.autoform.form import AutoObjectSubForm
from plone.dexterity.browser import edit
from plone.dexterity.interfaces import IDexterityEditForm
from plone.dexterity.utils import safe_unicode
from plone.supermodel import model
from plone.z3cform import layout
from z3c.form import button
from z3c.form import interfaces
from z3c.form.browser.object import ObjectWidget
from z3c.form.object import ObjectSubForm
from z3c.form.object import registerFactoryAdapter
from z3c.form.object import SubformAdapter
from zope import schema
from zope.annotation import IAnnotations
from zope.component import adapter
from zope.component import provideAdapter
from zope.interface import classImplements
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty


class IHarvesterSingleSchema(model.Schema):

    destination = schema.Choice(
        required=False,
        title=_(u'Destination'),
        source=DcatFieldVocabulary(),
    )

    form.widget(
        'query',
        SparqlQueryFieldWidget,
    )
    query = schema.Text(
        required=True,
        title=_(u'Query'),
        default=safe_unicode(QUERY_ATT_STR),
    )


@implementer(IHarvesterSingleSchema)
class HarvesterSingle(object):

    destination = FieldProperty(IHarvesterSingleSchema['destination'])
    query = FieldProperty(IHarvesterSingleSchema['query'])

registerFactoryAdapter(IHarvesterSingleSchema, HarvesterSingle)


class HarvesterSingleEntityForm(edit.DefaultEditForm):
    schema = IHarvesterSingleSchema
    additionalSchemata = []

    def getContent(self):
        annotations = IAnnotations(self.context)
        if HARVESTER_ENTITY_KEY in annotations:
            data = annotations[HARVESTER_ENTITY_KEY]
        else:
            data = {}
        default_query = QUERY_ATT_STR
        harvester = HarvesterSingle()
        harvester.query = default_query
        # field_id must be value used in vocabulary
        if self.request.form and 'field_id' in self.request.form:
            field_id = self.request.form['field_id']
            harvester.destination = field_id
            if field_id in data:
                harvester.query = data['field_id']

        return harvester

    @button.buttonAndHandler(_(u'Save'))
    def handle_submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        annotations = IAnnotations(self.context)
        if HARVESTER_ENTITY_KEY in annotations:
            stored_data = annotations[HARVESTER_ENTITY_KEY]
        else:
            stored_data = {}

        stored_data[data['destination']] = data['query']

        annotations[HARVESTER_ENTITY_KEY] = stored_data

        self.status = _(u'Thank you very much!')

HarvesterSingleEntityView = layout.wrap_form(HarvesterSingleEntityForm)
classImplements(HarvesterSingleEntityView, IDexterityEditForm)


class HarvesterSubForm(AutoObjectSubForm, ObjectSubForm):
    """Harvester Sub Form Object."""

    def __getattr__(self, name):
        try:
            return getattr(self.parentForm, name)
        except AttributeError:
            return super(HarvesterSubForm, self).__getattr__(name)


@implementer(interfaces.ISubformFactory)
@adapter(
    Interface,              # widget value
    interfaces.IFormLayer,  # request
    Interface,              # widget context
    Interface,              # form
    ObjectWidget,           # widget
    Interface,              # field
    Interface,              # field.schema
)
class HarvesterSubformAdapter(SubformAdapter):
    """Subform Adapter."""

    factory = HarvesterSubForm

provideAdapter(HarvesterSubformAdapter)


class IHarvesterMultiSchema(model.Schema):

    fields = schema.List(
        title=_('Select your fields'),
        value_type=schema.Object(
            required=True,
            title=_(u'Query'),
            schema=IHarvesterSingleSchema,
        ),
    )


# @implementer(IHarvesterMultiSchema)
# class HarvesterMulti(object):
#
#     def __init__(self, fields, context):
#         self.fields = fields
#         self.context = context
#
#     def absolute_url(self):
#         return self.context.absolute_url()
#
# registerFactoryAdapter(IHarvesterMultiSchema, HarvesterMulti)


class HarvesterMultiEntityForm(edit.DefaultEditForm):
    schema = IHarvesterMultiSchema
    additionalSchemata = []

    def getContent(self):
        annotations = IAnnotations(self.context)
        field_data = []
        if HARVESTER_ENTITY_KEY in annotations:
            data = annotations[HARVESTER_ENTITY_KEY]
            for el in data.keys():
                harv = HarvesterSingle()
                harv.destination = el
                harv.query = data[el]
                field_data.append(harv)

        return {'fields': field_data}

    @button.buttonAndHandler(_(u'Save'))
    def handle_submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        annotations = IAnnotations(self.context)

        stored_data = {}

        for obj in data['fields']:
            stored_data[obj.destination] = obj.query

        annotations[HARVESTER_ENTITY_KEY] = stored_data

        self.status = _(u'Thank you very much!')


HarvesterMultiEntityView = layout.wrap_form(HarvesterMultiEntityForm)
classImplements(HarvesterMultiEntityView, IDexterityEditForm)
