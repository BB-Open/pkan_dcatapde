# -*- coding: utf-8 -*-
"""A custom SPARQL Query widget."""
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFPlone.resources import add_resource_on_request
from Products.Five import BrowserView
from zope.interface import alsoProvides

import json


JS = """
    (function($) {
         $(document).ready(function() {

              $.ajax({
                  url: '%s',
                  method: 'GET',
                  dataType: 'json',
                  data: {},
                  success: displaygraph,
                  error: function() {alert('error getting data');}
              });
        });

        var displaygraph = function(data) {
            $('#cy').cytoscape({
                elements: data
            });
        }
    })(jQuery);
"""


class Graph(BrowserView):
    """A View for returning data for a cytoscape graph"""

    def __call__(self, *args, **kwargs):

        alsoProvides(self.request, IDisableCSRFProtection)
        add_resource_on_request(self.request, 'pkanpatterngraph')
#        add_resource_on_request(self.request, 'cytoscape')
        return super(Graph, self).__call__(*args, **kwargs)

    def graph_dcat_data(self, *args, **kwargs):
        """call me"""

        # fetch the RDF processor on the harvester
        processor = self.context.source_type(self.context)
        # run the processor and transform the result to JSON
        pretty = json.dumps(processor.parse_dact_data())
        # set the content type
        self.request.response.setHeader('Content-type', 'application/json')
        # return the JSON
        return pretty

    def graph_input_data(self, *args, **kwargs):
        """call me"""

        # fetch the RDF processor on the harvester
        processor = self.context.source_type(self.context)
        # run the processor and transform the result to JSON
        pretty = json.dumps(processor.parse_input_data())
        # set the content type
        self.request.response.setHeader('Content-type', 'application/json')
        # return the JSON
        return pretty

    def ajax_urls(self):
        dact_url = self.context.absolute_url() + '/graph_dcat_data'
        input_url = self.context.absolute_url() + '/graph_imput_data'

        result = {
            'dcat': dact_url,
            'input': input_url,
        }
        return result
