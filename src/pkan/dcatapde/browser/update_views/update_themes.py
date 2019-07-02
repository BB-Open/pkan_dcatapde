# -*- coding: utf-8 -*-
"""Test view for the import of Licenses"""

import rdflib
import surf

from pkan.dcatapde import _
from pkan.dcatapde.browser.update_views.update_base import UpdateObjectsBase
from pkan.dcatapde.constants import CT_SKOS_CONCEPT
from pkan.dcatapde.constants import FOLDER_CONCEPTS
from pkan.dcatapde.constants import VOCAB_SOURCES
from pkan.dcatapde.interfaces import IPKANImportSettings

from pkan.dcatapde.utils import (
    get_available_languages_iso,
    get_available_languages_title, )
from ps.zope.i18nfield.utils import get_default_language

from plone.api import content, portal
from zope.i18n import translate

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
        # get the surf license objects
        themes = self.load_objects_from_rdf()

        default_language = get_default_language()

        available_languages = get_available_languages_iso()
        available_languages_title = get_available_languages_title()

        count = 0
        for theme in themes:
            # map the properties
            mapping = {
                'dct_title': 'skos_prefLabel',
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
                        lang = getattr(literal, 'language', default_language)
                        lang = str(lang)
                        if lang in available_languages:
                            lang = available_languages[lang]
                        if lang not in available_languages_title:
                            continue
                        att_data[lang] = str(literal)
                else:
                    if not attribute.first:
                        att_data = None
                    else:
                        att_data = str(attribute.first)

                params[key] = att_data

            # Use subject as rdfabout
            att_data = str(getattr(theme, 'subject'))

            params['rdfs_isDefinedBy'] = att_data

            # Todo : Check for collisions. Probably not by title but by
            # rdfs_isDefinedBy

            if not params['dct_title']:
                params['dct_title'] = params['dc_identifier']

            # create a license document object
            try:
                if isinstance(params['dc_identifier'], list):
                    id = params['dc_identifier'][default_language]
                else:
                    id = params['dc_identifier']
                if isinstance(params['dc_title'], list):
                    title = params['dct_title'][default_language]
                else:
                    title = params['dct_title']

                content.create(
                    container=self.context,
                    type=CT_SKOS_CONCEPT,
                    id=id,
                    title=title,
                    **params)
            except Exception:
                continue
            else:
                count += 1

        msg = _('Imported ${count} concepts items.', mapping={
            'count': count,
        })
        msg = translate(msg, context=self.request)
        portal.show_message(message=msg, request=self.request)
        url = '/'.join([
            portal.get().absolute_url(),
            FOLDER_CONCEPTS,
        ])
        self.request.response.redirect(url)
        return u''
