# -*- coding: utf-8 -*-
"""Test view for the import of Licenses"""
from pkan.dcatapde.constants import CT_SKOS_CONCEPT
from pkan.dcatapde.constants import VOCAB_SOURCES
from plone.api import content
from plone.api import portal

import rdflib
import surf


surf.namespace.register(ADMS='http://www.w3.org/ns/adms#')


class UpdateThemes(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def load_themes_from_rdf(self):
        uri = VOCAB_SOURCES[CT_SKOS_CONCEPT]

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
        Theme = session.get_class(surf.ns.SKOS['Concept'])
        # Get the licenses objects
        themes = Theme.all().full()

        # Iterate over the licenses and yoiedl them
        return themes

    def __call__(self):
        # get the surf license objects
        themes = self.load_themes_from_rdf()

        default_language = portal.get_default_language()

        for theme in themes:
            # map the properties
            mapping = {
                'dct_title': 'skos_preflabel',
                'skos_inScheme': 'skos_inScheme',
                'dc_identifier': 'dc_identifier',
            }
            params = {}
            for key, value in mapping.items():
                attribute = getattr(theme, value)
                # deal wth more than one attribute, e.g. different languages
                #  in Literals
                if isinstance(attribute.first, rdflib.term.Literal):
                    att_data = {}
                    for literal in attribute:
                        # check if language attribute exists
                        try:
                            att_data[theme.language] = unicode(literal)
                        except AttributeError:
                            att_data[default_language] = unicode(literal)
                else:
                    att_data = unicode(attribute.first)

                params[key] = att_data

#            # Special case of adms_identifier. Target type is string not
#            # i18ntext. Therefore no dict but string has to be extracted
#            attribute = getattr(license, 'adms_identifier')
#            att_data = unicode(attribute.first)
#            params['adms_identifier'] = att_data

            # Use subject as rdfabout
            att_data = unicode(getattr(theme, 'subject'))

            params['rdfs_isDefinedBy'] = att_data

            # Todo : Check for collisions. Probably not by title but by
            # rdfs_isDefinedBy

            # create a license document object
            content.create(
                container=self.context,
                type=CT_SKOS_CONCEPT,
                id=params['dc_identifier'],
                title=params['dct_title'][default_language],
                **params)

            # Todo : Logging or response to user