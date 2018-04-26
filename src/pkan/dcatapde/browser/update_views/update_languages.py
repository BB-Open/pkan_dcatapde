# -*- coding: utf-8 -*-
"""Test view for the import of Licenses"""
from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DCT_LANGUAGE
from pkan.dcatapde.constants import FOLDER_LANGUAGES
from pkan.dcatapde.constants import VOCAB_SOURCES
from pkan.dcatapde.languages import AVAILABLE_LANGUAGES_ISO
from pkan.dcatapde.utils import get_default_language
from plone.api import content
from plone.api import portal
from rdflib import URIRef
from zope.i18n import translate

import os
import rdflib
import surf


surf.namespace.register(ADMS='http://www.w3.org/ns/adms#')


class UpdateLanguages(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def load_languages_from_rdf(self):
        uri = VOCAB_SOURCES[CT_DCT_LANGUAGE]

        if uri.startswith('http') or uri.startswith('/'):
            pass
        else:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            uri = os.path.join(dir_path, uri)

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
        Language = session.get_class(surf.ns.SKOS['Concept'])
        # Get the languages objects
        languages = Language.all().full()

        return languages

    def __call__(self):
        # get the surf license objects
        languages = self.load_languages_from_rdf()

        default_language = get_default_language()

        self.all_languages = []
        self.data = []

        for language in languages:
            # map the properties
            mapping = {
                'dct_title': 'skos_prefLabel',
                'rdfs_isDefinedBy': 'subject',
                'new_representation': 'dc_identifier',
            }

            params = {}
            for key, value in mapping.items():
                attribute = getattr(language, value)
                # deal wth more than one attribute, e.g. different languages
                #  in Literals
                if isinstance(attribute, URIRef):
                    att_data = str(attribute)
                elif isinstance(attribute.first, rdflib.term.Literal):
                    att_data = {}
                    for literal in attribute:
                        lang = getattr(literal, 'language', default_language)
                        lang = unicode(lang)
                        att_data[lang] = unicode(literal)
                else:
                    if not attribute.first:
                        att_data = None
                    else:
                        att_data = unicode(attribute.first.lower())

                if isinstance(att_data, dict) and \
                        len(att_data) == 1 and \
                        u'None' in att_data:
                    att_data = att_data[u'None'].lower()

                params[key] = att_data

            self.select_data(params)

        self.create_objects(self.data, self.all_languages)

    def select_data(self, params):
        # select data
        use_data = False
        if 'dct_title' not in params:
            return
        titles = params['dct_title'].copy()
        lang = params['new_representation']
        if not lang:
            return
        for key in params['dct_title'].keys():
            if len(key) == 3:
                if key == lang:
                    continue
                else:
                    use_data = True
            else:
                if key in AVAILABLE_LANGUAGES_ISO:
                    titles[AVAILABLE_LANGUAGES_ISO[key]] = titles[key]
                del titles[key]
        params['dct_title'] = titles

        if not use_data:
            return
        else:
            pass

        for short, long in AVAILABLE_LANGUAGES_ISO.iteritems():
            if long == lang:
                params['old_representation'] = short
                break

        if lang not in self.all_languages:
            self.all_languages.append(lang)
        self.data.append(params)

    def create_objects(self, data, all_languages):
        count = 0
        for params in data:
            # remove unused languages
            titles = params['dct_title'].copy()
            for key in params['dct_title'].keys():
                if key not in all_languages:
                    del titles[key]
            if len(titles) <= 1:
                continue
            params['dct_title'] = titles

            # create a license document object
            try:
                content.create(
                    container=self.context,
                    type=CT_DCT_LANGUAGE,
                    id=params['new_representation'],
                    **params)
            except Exception:
                continue
            else:
                count += 1

        msg = _('Imported ${count} DCT:Language items.', mapping={
            'count': count,
        })
        msg = translate(msg, context=self.request)
        portal.show_message(message=msg, request=self.request)
        url = '/'.join([
            portal.get().absolute_url(),
            FOLDER_LANGUAGES,
        ])
        self.request.response.redirect(url)
        return u''
