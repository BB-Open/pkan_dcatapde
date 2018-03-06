# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.browser.harvester_entity.preview import PreviewFormMixin
from pkan.dcatapde.vocabularies.dcat_field import DcatFieldVocabulary
from z3c.form import button
from z3c.form import field
from z3c.form.form import Form
from zope import schema
from zope.interface import Interface


class IHarvesterTestSchema(Interface):

    destination = schema.Choice(
        required=False,
        title=_(u'Destination'),
        source=DcatFieldVocabulary(),
    )

    query = schema.Text(
        required=True,
        title=_(u'Query'),
        default=u'Hello World',
    )

    preview = schema.Text(
        required=False,
        title=_(u'Preview'),
        readonly=True,
        default=_('No value'),
    )


class HarvesterTestView(Form, PreviewFormMixin):
    fields = field.Fields(IHarvesterTestSchema)
    query_attr = 'query'
    url_attr = None
    type_attr = None

    def getContent(self):
        return {}

    @button.buttonAndHandler(_(u'Save'))
    def handle_submit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.status = _(u'Thank you very much!')

    @button.buttonAndHandler(_(u'Run'))
    def handle_run(self, action):
        self.handle_preview()
