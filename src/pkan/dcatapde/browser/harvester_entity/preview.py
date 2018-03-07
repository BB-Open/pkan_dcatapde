# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_HARVESTER
from pkan.dcatapde.harvesting.source_type.rdfttl import IFaceToRDFFormatKey
from Products.Five import BrowserView

import json


class PreviewFormMixin(object):
    """
    Form Mixin to get preview of sparql query
    Provides methods to get preview

    Form has to provide a preview-Field
    """

    # set this attributes related to Form
    query_attr = 'query'
    url_attr = 'url'
    type_attr = 'type'

    def handle_preview(self, ignore_context=False):
        """
        Request preview and return it.
        :param ignore_context: usefull for forms where harvester parameter can
        be edited too eg. Edit and Add Form
        :return:
        """
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        if (self.context.portal_type == CT_HARVESTER and
                self.query_attr in data and
                ignore_context is False):
            value = self.update_preview_by_context(data[self.query_attr])
        elif (self.query_attr in data and
              self.type_attr in data and
              self.url_attr in data):

            value = self.update_preview_by_url_and_type(
                data[self.url_attr],
                data[self.type_attr],
                data[self.query_attr],
                ignore_context=ignore_context,
            )
        else:
            value = _(u'Could not request preview.')

        self.widgets['preview'].value = value

    def update_preview_by_context(self, query):
        self.request.form['query'] = query
        view = self.context.restrictedTraverse('@@harvester_preview')
        view = view.__of__(self.context)
        return view()

    def update_preview_by_url_and_type(self,
                                       url,
                                       type,
                                       query,
                                       ignore_context=False):
        # get rdf Format to create graph in preview view
        type_format = IFaceToRDFFormatKey[type]

        self.request.form['query'] = query
        self.request.form['rdf_url'] = url
        self.request.form['rdf_format'] = type_format
        self.request.form['ignore_context'] = ignore_context
        view = self.context.restrictedTraverse('@@harvester_preview')
        view = view.__of__(self.context)
        return view()


# class HarvesterPreview(BrowserView):
#
#     def __call__(self, *args, **kwargs):
#         context = self.context
#         query = None
#         url = None
#         rdf_format = None
#         ignore_context = False
#         if self.request.form:
#             if 'query' in self.request.form:
#                 query = self.request.form['query']
#             if 'source_path' in self.request.form:
#                 context = api.content.get(
#                     path=self.request.form['source_path'],
#                 )
#             if ('rdf_url' in self.request.form and
#                     'rdf_format' in self.request.form):
#                 url = self.request.form['rdf_url']
#                 rdf_format = self.request.form['rdf_format']
#             if 'ignore_context' in self.request.form:
#                 ignore_context = self.request.form['ignore_context']
#                 if (isinstance(ignore_context, str) and
#                         ignore_context == 'False'):
#                     ignore_context = False
#
#         source_type = getattr(context, 'source_type', None)
#         preview = _('Result: ')
#
#         graph = self.get_graph(source_type,
#                                url,
#                                ignore_context,
#                                query,
#                                context,
#                                rdf_format)
#
#         if graph is None:
#             return preview + \
#                 _(u' Did not find correct parameters to request data.')
#
#         try:
#             res = graph.query(query)
#         except ParseException:
#             preview += _(u'Wrong Syntax')
#         except SAXParseException:
#             preview += _(u'Could not read source.')
#         else:
#             # Todo: Sometimes None-Type is not iterable exception
#             preview += vkb.xml(res.serialize())
#
#         if preview and len(preview) > MAX_QUERY_PREVIEW_LENGTH:
#             preview = preview[:MAX_QUERY_PREVIEW_LENGTH] + '...'
#
#         return preview
#
#     def get_graph(self,
#                   source_type,
#                   url,
#                   ignore_context,
#                   query,
#                   context,
#                   rdf_format):
#         graph = None
#         if source_type and query and ignore_context is False:
#             try:
#                 source_adapter = source_type(context)
#                 graph = source_adapter.graph
#             except TypeError:
#                 pass
#             except ValueError:
#                 pass
#
#         if url and rdf_format and graph is None:
#             try:
#                 rdfstore = IOMemory()
#                 graph = Graph(rdfstore)
#                 graph.load(url,
#                            format=rdf_format)
#             except ValueError:
#                 pass
#         return graph


class HarvesterPreview(BrowserView):
    """View to get a preview of a harvester sparql query"""
    def __call__(self, *args, **kwargs):
        return self.get_preview

    @property
    def get_preview(self):
        processor = self.context.source_type(self.context)
        preview = processor.get_preview()
        pretty = json.dumps(preview)
        self.request.response.setHeader('Content-type', 'application/json')
        return pretty
