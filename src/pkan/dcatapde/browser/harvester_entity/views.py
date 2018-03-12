# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.constants import HARVESTER_DEFAULT_KEY
from pkan.dcatapde.constants import HARVESTER_DEXTERITY_KEY
from pkan.dcatapde.constants import HARVESTER_ENTITY_KEY
from pkan.dcatapde.structure.sparql import QUERY_ATT_STR
from pkan.dcatapde.vocabularies.dcat_field import DcatFieldVocabulary
from pkan.widgets.sparqlquery import SparqlQueryFieldWidget
from plone.app.z3cform.widget import AjaxSelectFieldWidget
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
        required=True,
        title=_(u'Destination'),
        source=DcatFieldVocabulary(),
    )

    form.widget(
        'query',
        SparqlQueryFieldWidget,
    )
    query = schema.Text(
        required=False,
        title=_(u'Query'),
        default=safe_unicode(QUERY_ATT_STR),
    )

    form.widget(
        'dext_object',
        AjaxSelectFieldWidget,
        initial_path='/',
    )
    dext_object = schema.Choice(
        required=False,
        title=_(u'Dexterity Object'),
        vocabulary='pkan.dcatapde.vocabularies.AllDcatObjects',
    )

    default = schema.TextLine(
        required=False,
        title=_(u'Default Value'),
    )


@implementer(IHarvesterSingleSchema)
class HarvesterSingle(object):

    destination = FieldProperty(IHarvesterSingleSchema['destination'])
    query = FieldProperty(IHarvesterSingleSchema['query'])
    dext_object = FieldProperty(IHarvesterSingleSchema['dext_object'])
    default = FieldProperty(IHarvesterSingleSchema['default'])

registerFactoryAdapter(IHarvesterSingleSchema, HarvesterSingle)


class HarvesterSingleEntityForm(edit.DefaultEditForm):
    schema = IHarvesterSingleSchema
    additionalSchemata = []

    def getContent(self):
        annotations = IAnnotations(self.context)
        if HARVESTER_ENTITY_KEY in annotations:
            sparql = annotations[HARVESTER_ENTITY_KEY]
        else:
            sparql = {}
        if HARVESTER_DEXTERITY_KEY in annotations:
            dexterity = annotations[HARVESTER_DEXTERITY_KEY]
        else:
            dexterity = {}
        if HARVESTER_DEFAULT_KEY in annotations:
            default = annotations[HARVESTER_DEFAULT_KEY]
        else:
            default = {}
        default_query = QUERY_ATT_STR
        harvester = HarvesterSingle()
        harvester.query = default_query
        # field_id must be value used in vocabulary
        if self.request.form and 'field_id' in self.request.form:
            field_id = self.request.form['field_id']
            harvester.destination = field_id
            if field_id in sparql:
                harvester.query = sparql[field_id]
            if field_id in dexterity:
                harvester.dext_object = dexterity[field_id]
            if field_id in default:
                harvester.default = default[field_id]

        return harvester

    @button.buttonAndHandler(_(u'Save'))
    def handle_submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        annotations = IAnnotations(self.context)
        if HARVESTER_ENTITY_KEY in annotations:
            sparql = annotations[HARVESTER_ENTITY_KEY]
        else:
            sparql = {}
        if HARVESTER_DEXTERITY_KEY in annotations:
            dexterity = annotations[HARVESTER_DEXTERITY_KEY]
        else:
            dexterity = {}
        if HARVESTER_DEFAULT_KEY in annotations:
            default = annotations[HARVESTER_DEFAULT_KEY]
        else:
            default = {}

        if data['query']:
            sparql[data['destination']] = data['query']
        if data['dext_object']:
            dexterity[data['destination']] = data['dext_object']
        if data['default']:
            default[data['destination']] = data['default']

        annotations[HARVESTER_ENTITY_KEY] = sparql
        annotations[HARVESTER_DEXTERITY_KEY] = dexterity
        annotations[HARVESTER_DEFAULT_KEY] = default

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
            sparql = annotations[HARVESTER_ENTITY_KEY]
        else:
            sparql = {}
        if HARVESTER_DEXTERITY_KEY in annotations:
            dexterity = annotations[HARVESTER_DEXTERITY_KEY]
        else:
            dexterity = {}
        if HARVESTER_DEFAULT_KEY in annotations:
            default = annotations[HARVESTER_DEFAULT_KEY]
        else:
            default = {}

        keys = set(default.keys() + dexterity.keys() + sparql.keys())

        for field_id in keys:
            harv = HarvesterSingle()
            harv.destination = field_id
            if field_id in sparql:
                harv.query = sparql[field_id]
            else:
                harv.query = QUERY_ATT_STR
            if field_id in dexterity:
                harv.dext_object = dexterity[field_id]
            if field_id in default:
                harv.default = default[field_id]
            field_data.append(harv)

        return {'fields': field_data}

    @button.buttonAndHandler(_(u'Save'))
    def handle_submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        annotations = IAnnotations(self.context)

        sparql = {}
        dexterity = {}
        default = {}

        for obj in data['fields']:
            if obj.query:
                sparql[obj.destination] = obj.query
            if obj.dext_object:
                dexterity[obj.destination] = obj.dext_object
            if obj.default:
                default[obj.destination] = obj.default

        annotations[HARVESTER_ENTITY_KEY] = sparql
        annotations[HARVESTER_DEXTERITY_KEY] = dexterity
        annotations[HARVESTER_DEFAULT_KEY] = default

        self.status = _(u'Thank you very much!')


HarvesterMultiEntityView = layout.wrap_form(HarvesterMultiEntityForm)
classImplements(HarvesterMultiEntityView, IDexterityEditForm)
