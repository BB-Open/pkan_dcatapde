# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.browser.harvester_entity.preview import PreviewFormMixin
from pkan.dcatapde.constants import HARVESTER_ENTITY_KEY
from pkan.dcatapde.structure.sparql import QUERY_ATT_STR
from pkan.dcatapde.vocabularies.dcat_field import DcatFieldVocabulary
from plone.dexterity.utils import safe_unicode
from z3c.form import button
from z3c.form import field
from z3c.form.form import Form
from zope import schema
from zope.annotation import IAnnotations
from zope.interface import Interface


class IHarvesterSingleSchema(Interface):

    destination = schema.Choice(
        required=False,
        title=_(u'Destination'),
        source=DcatFieldVocabulary(),
    )

    query = schema.Text(
        required=True,
        title=_(u'Query'),
        default=safe_unicode(QUERY_ATT_STR),
    )

    preview = schema.Text(
        required=False,
        title=_(u'Preview'),
        readonly=True,
        default=_('No value'),
    )


class IHarvesterMultiSchema(Interface):

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


class HarvesterSingleEntityView(Form, PreviewFormMixin):
    fields = field.Fields(IHarvesterSingleSchema)
    query_attr = 'query'
    url_attr = None
    type_attr = None

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

    @button.buttonAndHandler(_(u'Run'))
    def handle_run(self, action):
        self.handle_preview()


class HarvesterMultiEntityView(Form, PreviewFormMixin):
    fields = field.Fields(IHarvesterMultiSchema)
    query_attr = 'query'
    url_attr = None
    type_attr = None

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
