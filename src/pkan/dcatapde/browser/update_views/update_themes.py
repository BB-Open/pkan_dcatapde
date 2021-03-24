# -*- coding: utf-8 -*-
"""Test view for the import of Licenses"""
from pkan.dcatapde import _
from pkan.dcatapde import constants
from pkan.dcatapde.browser.update_views.update_base import UpdateObjectsBase
from pkan.dcatapde.constants import CT_SKOS_CONCEPT
from pkan.dcatapde.constants import FOLDER_CONCEPTS
from pkan.dcatapde.interfaces import IPKANImportSettings
from pkan.dcatapde.utils import get_available_languages_iso
from pkan.dcatapde.utils import get_available_languages_title
from plone.api import content
from plone.api import portal
from ps.zope.i18nfield.utils import get_default_language
from zope.i18n import translate

import rdflib
import surf


MAPPING = {
    'dct_title': 'skos_prefLabel',
    'skos_inScheme': 'skos_inScheme',
    'dc_identifier': 'dc_identifier',
}


class UpdateThemes(UpdateObjectsBase):

    uri_registry_key = CT_SKOS_CONCEPT
    uri_registry_interface = IPKANImportSettings
    object_class = surf.ns.SKOS['Concept']
    object_title = 'skos:concepts'
    object_dx_class = CT_SKOS_CONCEPT
    target_folder = FOLDER_CONCEPTS
    mapping = MAPPING

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        # get the surf theme objects
        themes = self.load_objects_from_rdf()

        self.default_language = get_default_language()

        self.available_languages = get_available_languages_iso()
        self.available_languages_title = get_available_languages_title()

        # map the properties
        self.mapping = {
            'dct_title': 'skos_prefLabel',
            'skos_inScheme': 'skos_inScheme',
            'dc_identifier': 'dc_identifier',
        }
        self.count = 0
        for theme in themes:
            self.update(theme)

        msg = _('Imported ${count} concepts items.', mapping={
            'count': self.count,
        })
        msg = translate(msg, context=self.request)
        portal.show_message(message=msg, request=self.request)
        url = '/'.join([
            portal.get().absolute_url(),
            FOLDER_CONCEPTS,
        ])
        self.request.response.redirect(url)
        return u''

    def update(self, theme):
        params = {}
        for key, value in self.mapping.items():
            attribute = getattr(theme, value)
            # deal wth more than one attribute, e.g. different languages
            #  in Literals
            if isinstance(attribute.first, rdflib.term.Literal):
                att_data = {}
                for literal in attribute:
                    lang = getattr(literal, 'language', self.default_language)
                    lang = str(lang)
                    if lang in self.available_languages:
                        lang = self.available_languages[lang]
                        att_data[lang] = str(literal)
                if not att_data:
                    att_data = str(attribute.first)
            else:
                if not attribute.first:
                    att_data = None
                else:
                    att_data = str(attribute.first)

            params[key] = att_data

        # Use subject as rdfabout
        att_data = str(getattr(theme, 'subject'))

        params['rdfs_isDefinedBy'] = att_data

        params = self.get_foaf_depiction(params, att_data)

        # Todo : Check for collisions. Probably not by title but by
        # rdfs_isDefinedBy

        if not params['dct_title']:
            params['dct_title'] = params['dc_identifier']

        # create a skos:concept object
        try:
            if isinstance(params['dc_identifier'], dict):
                id = params['dc_identifier'][self.default_language]
            else:
                id = params['dc_identifier']
            if isinstance(params['dct_title'], dict):
                title = params['dct_title'][self.default_language]
            else:
                title = params['dct_title']

            content.create(
                container=self.context,
                type=CT_SKOS_CONCEPT,
                id=id,
                title=title,
                **params)
        except Exception as e:  # noqa: B902
            portal.show_message(message=str(e), request=self.request)
            return
        else:
            self.count += 1

    def get_foaf_depiction(self, params, att_data):
        FOAF_DEPICTION = constants.VOCAB_SOURCES[constants.CT_SKOS_CONCEPT]

        try:
            params['foaf_depiction'] = FOAF_DEPICTION[att_data]
        except KeyError:
            # no image provided
            pass

        return params
