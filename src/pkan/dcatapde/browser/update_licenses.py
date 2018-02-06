# -*- coding: utf-8 -*-
"""Test view for the import of Licenses"""
from pkan.dcatapde.constants import CT_DCT_LICENSE_DOCUMENT
from pkan.dcatapde.constants import VOCAB_SOURCES
from plone.api import content
from plone.api import portal

import rdflib
import surf


surf.namespace.register(ADMS='http://www.w3.org/ns/adms#')


class UpdateLicenses(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def load_licenses_from_rdf(self):
        uri = VOCAB_SOURCES[CT_DCT_LICENSE_DOCUMENT]

        store = surf.Store(
            reader='rdflib',
            writer='rdflib',
            rdflib_store='IOMemory',
        )
        # Get a new surf session
        session = surf.Session(store)
        # Load the license list
        store.load_triples(source=uri)
        # Define the License class as an owl:class object
        License = session.get_class(surf.ns.OWL['Class'])
        # Get the licenses objects
        licenses = License.all().full()

        # Iterate over the licenses and yoiedl them
        return licenses

    def __call__(self):
        # get the surf license objects
        licenses = self.load_licenses_from_rdf()

        default_language = portal.get_default_language()

        for license in licenses:
            # map the properties
            mapping = {
                'dct_title': 'rdfs_label',
                'dct_description': 'rdfs_comment',
                'rdfs_subClassOf': 'rdfs_subClassOf',
            }
            params = {}
            for key, value in mapping.items():
                attribute = getattr(license, value)
                # deal wth more than one attribute, e.g. different languages
                #  in Literals
                if isinstance(attribute.first, rdflib.term.Literal):
                    att_data = {}
                    for literal in attribute:
                        # check if language attribute exists
                        try:
                            att_data[literal.language] = unicode(literal)
                        except AttributeError:
                            att_data[default_language] = unicode(literal)
                else:
                    att_data = unicode(attribute.first)

                params[key] = att_data

            # Special case of adms_identifier. Target type is string not
            # i18ntext. Therefore no dict but string has to be extracted
            attribute = getattr(license, 'adms_identifier')
            att_data = unicode(attribute.first)
            params['adms_identifier'] = att_data

            # Special case of isDefiendBy. If not given use rdfabout URI
            attribute = getattr(license, 'rdfs_isDefinedBy')
            if attribute:
                att_data = unicode(attribute.first)
            else:
                att_data = unicode(getattr(license, 'subject'))

            params['rdfs_isDefinedBy'] = att_data

            # Todo : Check for collisions. Probably not by title but by
            # rdfs_isDefinedBy

            # create a license document object
            content.create(
                container=self.context,
                type=CT_DCT_LICENSE_DOCUMENT,
                id=params['adms_identifier'],
                title=params['dct_description'][default_language],
                **params)

            # Todo : Logging or response to user