# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_HARVESTER
from pkan.dcatapde.constants import HARVESTER_FOLDER_ID
from pkan.dcatapde.constants import HARVESTER_FOLDER_TITLE
from pkan.dcatapde.content.harvester import Harvester
from pkan.dcatapde.vocabularies.source_type_vocab import SourceTypeVocabFactory
from plone import api
from Products.Five import BrowserView

import json


class HarvesterPreview(BrowserView):
    """View to get a preview of a harvester sparql query"""
    def __call__(self, *args, **kwargs):
        return self.get_preview

    @property
    def get_preview(self):

        # used for for add/edit-forms where url can be changed in form
        url = None
        # used for for context-free views to get harvester
        source_path = None
        # query to be used
        query = None
        # used for for add/edit-forms where source_type can be changed in form
        source_type = None
        # used to give context information to sparqle query
        bindings = {}

        if self.request.form:
            form = self.request.form
            if 'form.widgets.url' in form:
                url = form['form.widgets.url']
            if 'source_path' in form:
                source_path = form['source_path']
            if 'query_data' in form:
                query = form['query_data']
            if 'form.widgets.source_type' in form:
                source_type_token = form['form.widgets.source_type'][0]
                vocab = SourceTypeVocabFactory(self.context)
                terms = vocab.by_token
                term = terms[source_type_token]
                source_type = term.value
            if 'subject' in form:
                bindings['s'] = form['subject']
            if 'object' in form:
                bindings['o'] = form['object']
            if 'predicate' in form:
                bindings['p'] = form['predicate']

        context = self.get_preview_context(
            source_path,
            url,
            source_type,
        )

        if not context:
            return json.dumps(
                _(u'Did not find correct parameters to request data.'),
            )

        processor = context.source_type(context)
        preview = processor.get_preview(query, bindings=bindings)
        self.request.response.setHeader('Content-type', 'application/html')
        return preview

    def create_harvester(self, url, source_type):
        """
        Creating a pseudo harvester for adpater
        :param url:
        :param source_type:
        :return:
        """
        harvester = Harvester()
        harvester.id = HARVESTER_FOLDER_ID
        harvester.title = HARVESTER_FOLDER_TITLE
        harvester.url = url
        harvester.rdf_format = source_type

        return harvester

    def get_preview_context(self, source_path, url, source_type):
        if source_path:
            context = api.content.get(path=source_path)
        elif (self.context.portal_type == CT_HARVESTER):
            context = self.context
        else:
            context = None

        if url and source_type:
            if not context:
                context = self.create_harvester(url, source_type)
            elif context.url != url or context.source_type != source_type:
                # in case of add or edit-view fields could have changed
                context = self.create_harvester(url, source_type)

        return context
