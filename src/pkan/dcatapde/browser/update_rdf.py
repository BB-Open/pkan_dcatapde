# -*- coding: utf-8 -*-
"""Test view for the import of Licenses"""
from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.harvesting.RDF.surf_config import SC_DCAT_CATALOG
from pkan.dcatapde.marshall.target.rdf_store import RDFStore
from plone.api import content
from plone.api import portal

import rdflib


class UpdateRDF(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def load_rdf(self):

        #        uri = 'https://www.govdata.de/ckan/dataset/deutsche
        # -nationalbibliografie-dnb.rdf'
        #        uri = 'file:///home/volker/Downloads/examples/dcat_ap_de' \
        #              '-RefImp_RDF_MAX_V1.0.rdf'
        uri = 'file:///home/volker/Downloads/RDF/self.rdf'

        store = RDFStore()
        # Get a new surf session
        session = store.session
        # Load the license list
        store.load_triples(source=uri)

        # Iterate over the licenses and yoiedl them
        return session

    def __call__(self):
        # get the surf license objects
        session = self.load_rdf()

        default_language = portal.get_default_language()

        # Define the License class as an owl:class object
        Catalog = session.get_class(SC_DCAT_CATALOG)
        # Get the licenses objects
        catalogs = Catalog.all().full()

        for catalog in catalogs:
            # map the properties
            mapping = {
                'dct_title': 'dct_title',
                'dct_description': 'dct_description',
                'dct_publisher': 'dct_publisher',
            }
            params = {}
            for key, value in mapping.items():
                attribute = getattr(catalog, value)
                # deal wth more than one attribute, e.g. different languages
                #  in Literals
                if isinstance(attribute.first, rdflib.term.Literal):
                    att_data = {}
                    for literal in attribute:
                        # check if language attribute exists
                        try:
                            att_data[catalog.language] = unicode(literal)
                        except AttributeError:
                            att_data[default_language] = unicode(literal)
                else:
                    att_data = unicode(attribute.first)

                params[key] = att_data

            # Todo : Check for collisions. Probably not by title but by
            # rdfs_isDefinedBy

            # create a license document object
            content.create(
                container=self.context,
                type=CT_DCAT_DATASET,
                title=params['dct_title'][default_language],
                **params)

            # Todo : Logging or response to user
