# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.constants import MAX_QUERY_PREVIEW_LENGTH
from pkan.dcatapde.vocabularies.dcat_field import DcatFieldVocabulary
from plone import api
from Products.Five import BrowserView
from pyparsing import ParseException
from xml.sax import SAXParseException
from z3c.form import button
from z3c.form import field
from z3c.form.form import Form
from zope import schema
from zope.interface import Interface

import vkbeautify as vkb


class IHarvesterTestSchema(Interface):

    destination = schema.Choice(
        required=False,
        title=_(u'Destination'),
        source=DcatFieldVocabulary(),
    )

    prio = schema.Int(
        required=True,
        title=_(u'Priority'),
        default=1,
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


class HarvesterTestView(Form):
    fields = field.Fields(IHarvesterTestSchema)

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
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        self.update_preview(data['query'])

    def update_preview(self, query):
        self.request.form['query'] = query
        view = self.context.restrictedTraverse('@@harvester_preview')
        view = view.__of__(self.context)
        self.widgets['preview'].value = view()


class HarvesterPreview(BrowserView):

    def __call__(self, *args, **kwargs):
        context = self.context
        query = None
        if self.request.form and 'query' in self.request.form:
            query = self.request.form['query']
        if self.request.form and 'source_path' in self.request.form:
            context = api.content.get(path=self.request.form['source_path'])

        source_type = getattr(context, 'source_type', None)
        preview = _(u'Not Found')

        if source_type and query:
            try:
                source_adapter = source_type(context)
            except TypeError:
                return preview

            try:
                res = source_adapter.run_query(query)
            except ParseException:
                preview = _(u'Wrong Syntax')
            except SAXParseException:
                preview = _(u'Could not read source.')
            else:
                # Todo: Sometimes None-Type is not iterable exception
                preview = vkb.xml(res.serialize())

            if preview and len(preview) > MAX_QUERY_PREVIEW_LENGTH:
                preview = preview[:MAX_QUERY_PREVIEW_LENGTH] + '...'

        return preview
