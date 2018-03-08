# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.constants import HARVESTER_ENTITY_KEY
from pkan.dcatapde.structure.sparql import QUERY_ATT_STR
from pkan.dcatapde.vocabularies.dcat_field import DcatFieldVocabulary
from pkan.widgets.sparqlquery import SparqlQueryFieldWidget
from plone.autoform import directives as form
from plone.autoform.form import AutoExtensibleForm
from plone.dexterity.browser import edit
from plone.dexterity.interfaces import IDexterityEditForm
from plone.dexterity.utils import safe_unicode
from plone.supermodel import model
from plone.z3cform import layout
from z3c.form import button
from z3c.form.form import Form
from zope import schema
from zope.annotation import IAnnotations
from zope.interface import classImplements


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
        # field_id must be value used in vocabulary
        if self.request.form and 'field_id' in self.request.form:
            field_id = self.request.form['field_id']
            if field_id in data:
                return {
                    'destination': field_id,
                    'query': data[field_id],
                }
            else:
                return {
                    'destination': field_id,
                    'query': default_query,
                }
        else:
            return {}

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


class IHarvesterMultiSchema(model.Schema):

    fields = schema.Dict(
        title=_('Select your fields'),

        key_type=schema.Choice(
            required=False,
            title=_(u'Destination'),
            source=DcatFieldVocabulary(),
        ),
        value_type=schema.Text(
            required=True,
            title=_(u'Query'),
            default=safe_unicode(QUERY_ATT_STR),

        ),
    )


class HarvesterMultiEntityView(AutoExtensibleForm, Form):
    schema = IHarvesterMultiSchema

    def getContent(self):
        annotations = IAnnotations(self.context)
        if HARVESTER_ENTITY_KEY in annotations:
            data = annotations[HARVESTER_ENTITY_KEY]
        else:
            data = {}

        return {'fields': data}

    @button.buttonAndHandler(_(u'Save'))
    def handle_submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        annotations = IAnnotations(self.context)

        stored_data = data['fields']

        annotations[HARVESTER_ENTITY_KEY] = stored_data

        self.status = _(u'Thank you very much!')

    @button.buttonAndHandler(_(u'Run'))
    def handle_run(self, action):
        # self.handle_preview()
        pass
