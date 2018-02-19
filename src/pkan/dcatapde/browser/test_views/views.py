# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.vocabularies.dcat_field import DcatFieldVocabulary
from plone import api
from Products.Five import BrowserView
from z3c.form import button
from z3c.form import field
from z3c.form.form import Form
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import Interface


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
    ignoreContext = True

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

        self.update_preview()

    def update_preview(self):
        view = getMultiAdapter((self.context, self.request),
                               name='harvester_preview')
        self.widgets['preview'].value = view()


class HarvesterPreview(BrowserView):

    def __call__(self, *args, **kwargs):
        context = self.context
        query = 'huhu'
        if self.request.form and 'form.widgets.query' in self.request.form:
            query = self.request.form['form.widgets.query']
        if self.request.form and 'source_path' in self.request.form:
            context = api.content.get(path=self.request.form['source_path'])

        url = getattr(context, 'url', None)

        if url and query:
            # Todo Sparkle Query here
            preview = 'Url: {url}, Query: {query}'.format(url=url, query=query)
        else:
            preview = 'Not Found'

        return preview
