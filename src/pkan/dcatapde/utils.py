# -*- coding: utf-8 -*-
"""Utilities."""
from pkan.dcatapde.constants import CT_LANGUAGE_FOLDER
from pkan.dcatapde.constants import FOLDER_LANGUAGES
from pkan.dcatapde.languages import AVAILABLE_LANGUAGES_ISO
from pkan.dcatapde.languages import AVAILABLE_LANGUAGES_TITLE
from pkan.dcatapde.languages import DEFAULT_LANGUAGE
from plone import api
from plone.api import portal
from ps.zope.i18nfield.interfaces import ILanguageAvailability
from ps.zope.i18nfield.plone.utils import LanguageAvailability
from zope.annotation.interfaces import IAnnotations
from zope.component import queryUtility
from zope.globalrequest import getRequest
from zope.interface import implementer


@implementer(ILanguageAvailability)
class PKANLanguages(LanguageAvailability):
    """A list of available languages."""

    @property
    def language_folder(self):
        # todo: Caching
        catalog = api.portal.get_tool('portal_catalog')
        results = catalog.searchResults(**{'portal_type': CT_LANGUAGE_FOLDER,
                                           'title': FOLDER_LANGUAGES})
        if not results:
            return None
        else:
            return results[0].getObject()

    @property
    def available_languages_iso(self):
        # todo: Caching
        if not self.language_folder or not self.language_folder.contentItems():
            return AVAILABLE_LANGUAGES_ISO
        res = {}
        for id, element in self.language_folder.contentItems():
            if getattr(element, 'old_representation', None):
                res[element.old_representation] = element.new_representation
        return res

    @property
    def avaible_languages_title(self):
        # todo: Caching
        if not self.language_folder or not self.language_folder.contentItems():
            return AVAILABLE_LANGUAGES_ISO
        res = {}
        for id, obj in self.language_folder.contentItems():
            if getattr(obj, 'new_representation', None):
                title = obj.Title()
                if title:
                    res[obj.new_representation] = title
                else:
                    res[obj.new_representation] = obj.new_representation
        return res

    def getAvailableLanguages(self, combined=False):
        """Return a sequence of language tags for available languages."""
        res = self.avaible_languages_title.keys()
        return res

    def getDefaultLanguage(self):
        """Return the system default language."""
        res = unicode(super(PKANLanguages, self).getDefaultLanguage())
        if res in self.available_languages_iso:
            return self.available_languages_iso[unicode(res)]
        else:
            return DEFAULT_LANGUAGE

    def getLanguages(self, combined=False):
        """Return a sequence of Language objects for available languages."""
        res = {}

        for lang in self.avaible_languages_title.keys():
            res[lang] = {u'name': self.avaible_languages_title[lang]}

        return res

    def getLanguageListing(self, combined=False):
        """Return a sequence of language code and language name tuples."""
        res = []
        for lang in self.avaible_languages_title.keys():
            res.append((lang, self.avaible_languages_title[lang]))
        return res


def get_request_annotations(key, request=None, default=None):
    """Get request data, stored in request annotations."""
    if request is None:
        request = getRequest()
    try:
        annotations = IAnnotations(request)
    except TypeError:
        return default
    else:
        return annotations.get(key, default)


def set_request_annotations(key, data, request=None):
    """Store a key, value pair of data in request annotations."""
    if request is None:
        request = getRequest()
    try:
        annotations = IAnnotations(request)
    except TypeError:
        return None
    else:
        annotations[key] = data
        return True


def get_default_language():
    lang = unicode(portal.get_default_language()[:2])
    languages = get_available_languages_iso()
    if lang in languages:
        def_lang = languages[lang]
    else:
        def_lang = DEFAULT_LANGUAGE

    return def_lang


def get_current_language():
    lang = unicode(portal.get_current_language()[:2])
    languages = get_available_languages_iso()
    if lang in languages:
        cur_lang = languages[lang]
    else:
        cur_lang = DEFAULT_LANGUAGE

    return cur_lang


def get_available_languages_iso():
    utility = queryUtility(ILanguageAvailability)
    if utility is not None and getattr(utility, 'available_languages_iso',
                                       None):
        languages = utility.available_languages_iso
    else:
        languages = AVAILABLE_LANGUAGES_ISO
    return languages


def get_available_languages_title():
    utility = queryUtility(ILanguageAvailability)
    if utility is not None and getattr(utility, 'available_languages_title',
                                       None):
        languages = utility.available_languages_title
    else:
        languages = AVAILABLE_LANGUAGES_TITLE
    return languages
