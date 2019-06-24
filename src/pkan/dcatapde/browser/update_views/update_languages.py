# -*- coding: utf-8 -*-
"""Test view for the import of Licenses"""
from pkan.dcatapde.browser.update_views.update_base import UpdateObjectsBase
from pkan.dcatapde.constants import CT_DCT_LANGUAGE
from pkan.dcatapde.constants import FOLDER_LANGUAGES
from pkan.dcatapde.constants import VOCAB_SOURCES
from pkan.dcatapde.languages import AVAILABLE_LANGUAGES_ISO
from plone.api import content
from plone.i18n.normalizer import idnormalizer
from zExceptions import BadRequest

import surf


surf.namespace.register(ADMS='http://www.w3.org/ns/adms#')

# map the properties
MAPPING = mapping = {
    'dct_title': 'skos_prefLabel',
    'rdfs_isDefinedBy': 'subject',
    'new_representation': 'dc_identifier',
}


class UpdateLanguages(UpdateObjectsBase):

    uri = VOCAB_SOURCES[CT_DCT_LANGUAGE]
    object_title = 'DCT:Language'
    object_dx_class = CT_DCT_LANGUAGE
    target_folder = FOLDER_LANGUAGES
    mapping = MAPPING

    def import_objects(self, objects):
        good_count = 0
        ignored_count = 0

        self.all_languages = []
        self.data = []

        for obj in objects:
            params = self.import_object(obj)
            # special case, should be string not dict
            if 'new_representation' in params:
                lang = params['new_representation'].values()[0].lower()
                params['new_representation'] = lang
            else:
                params['new_representation'] = None

            # Special case of adms_identifier. Target type is string not
            # i18ntext. Therefore no dict but string has to be extracted
            attribute = getattr(obj, 'dc_identifier')
            att_data = str(attribute.first)
            params['dc_identifier'] = att_data

            # Special case of isDefiendBy. If not given use rdfabout URI
            attribute = getattr(obj, 'rdfs_isDefinedBy')
            if attribute:
                att_data = str(attribute.first)
            else:
                att_data = str(getattr(obj, 'subject'))

            params['rdfs_isDefinedBy'] = att_data

            # Todo : Check for collisions. Probably not by title but by
            # rdfs_isDefinedBy

            # if there is no title use the identifier
            if not params['dct_title']:
                params['dct_title'] = params['dc_identifier']

            used = self.select_data(params)
            if not used:
                ignored_count += 1

        good_count, ignored_count = self.create_objects(good_count,
                                                        ignored_count)
        return good_count, ignored_count

    def select_data(self, params):
        # select data
        use_data = False
        if 'dct_title' not in params:
            return use_data
        elif isinstance(params['dct_title'], str):
            return use_data
        titles = params['dct_title'].copy()
        lang = params['new_representation']
        if not lang:
            return use_data
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
            return use_data

        for short, long in AVAILABLE_LANGUAGES_ISO.iteritems():
            if long == lang:
                params['old_representation'] = short
                break

        if lang not in self.all_languages:
            self.all_languages.append(lang)
        self.data.append(params)
        return use_data

    def create_objects(self, good_count, ignored_count):
        for params in self.data:
            titles = params['dct_title'].copy()
            for key in params['dct_title'].keys():
                if key not in self.all_languages:
                    del titles[key]
            if len(titles) <= 1:
                ignored_count += 1
                continue
            params['dct_title'] = titles

            if isinstance(params['dc_identifier'], dict):
                id = params['dc_identifier'][self.default_language]
            else:
                id = params['dc_identifier']
            id = idnormalizer.normalize(id)

            if isinstance(params['dct_title'], dict):
                title = params['dct_title'][self.default_language]
            else:
                title = params['dct_title']

            try:
                # create a license document object
                content.create(
                    container=self.context,
                    type=self.object_dx_class,
                    id=id,
                    title=title,
                    **params)
            # skip already existing licenses
            except BadRequest:
                ignored_count += 1
                continue
            else:
                good_count += 1
        return good_count, ignored_count
