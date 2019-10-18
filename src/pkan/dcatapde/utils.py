# -*- coding: utf-8 -*-
"""Utilities."""
from collections import OrderedDict
from DateTime.DateTime import time
from pkan.dcatapde.api.functions import query_active_objects
from pkan.dcatapde.constants import CT_DCT_LANGUAGE
from pkan.dcatapde.constants import CT_LANGUAGE_FOLDER
from pkan.dcatapde.constants import FOLDER_LANGUAGES
from pkan.dcatapde.constants import LANGUAGE_CACHE_TIMEOUT
from pkan.dcatapde.languages import AVAILABLE_LANGUAGES_ISO
from pkan.dcatapde.languages import AVAILABLE_LANGUAGES_TITLE
from pkan.dcatapde.languages import DEFAULT_LANGUAGE
from plone import api
from plone.api import portal
from plone.memoize import ram
from ps.zope.i18nfield.interfaces import ILanguageAvailability
from ps.zope.i18nfield.plone.utils import LanguageAvailability
from zope.annotation.interfaces import IAnnotations
from zope.component import queryUtility
from zope.globalrequest import getRequest
from zope.interface import implementer


def cache_key_iso(func, self):
    """cache key factory for lamguage isos.
    :param func:
    :param self:
    :return:
    """
    key = u'{0}_language_iso'.format(
        time() // LANGUAGE_CACHE_TIMEOUT,
    )
    return key


def cache_key_title(func, self):
    """cache key factory for language titles.
    :param func:
    :param self:
    :return:
    """
    key = u'{0}_language_title'.format(
        time() // LANGUAGE_CACHE_TIMEOUT,
    )
    return key


@implementer(ILanguageAvailability)
class PKANLanguages(LanguageAvailability):
    """A list of available languages."""

    @property
    def language_folder(self):
        results = api.content.find(**{'portal_type': CT_LANGUAGE_FOLDER,
                                      'title': FOLDER_LANGUAGES})
        if not results:
            return None
        else:
            return results[0].getObject()

    @property
    @ram.cache(cache_key_iso)
    def available_languages_iso(self):
        brains = query_active_objects({}, CT_DCT_LANGUAGE)
        if not brains:
            return AVAILABLE_LANGUAGES_ISO
        res = OrderedDict()
        for brain in brains:
            element = brain.getObject()
            if getattr(element, 'old_representation', None):
                res[element.old_representation] = element.new_representation
        return res

    @property
    @ram.cache(cache_key_title)
    def avaible_languages_title(self):
        brains = query_active_objects({}, CT_DCT_LANGUAGE)
        if not brains:
            res = AVAILABLE_LANGUAGES_TITLE
        else:
            res = OrderedDict()
            for brain in brains:
                obj = brain.getObject()
                if getattr(obj, 'new_representation', None):
                    title = obj.Title()
                    if title:
                        res[obj.new_representation] = title
                    else:
                        res[obj.new_representation] = obj.new_representation
        res = OrderedDict(sorted(res.items(), key=lambda x: x[1]))
        return res

    def getAvailableLanguages(self, combined=False):
        """Return a sequence of language tags for available languages."""
        res = list(self.avaible_languages_title.keys())
        return res

    def getDefaultLanguage(self):
        """Return the system default language."""
        res = str(super(PKANLanguages, self).getDefaultLanguage())
        if res in self.available_languages_iso:
            return self.available_languages_iso[str(res)]
        else:
            return DEFAULT_LANGUAGE

    def getLanguages(self, combined=False):
        """Return a sequence of Language objects for available languages."""
        res = OrderedDict()

        for lang in self.avaible_languages_title.keys():
            res[lang] = {u'name': self.avaible_languages_title[lang]}
        return res

    def getLanguageListing(self, combined=False):
        """Return a sequence of language code and language name tuples."""
        res = []
        for lang in self.avaible_languages_title.keys():
            res.append((lang, self.avaible_languages_title[lang]))
        return res

    def get_sorted_languages(self):
        return self.getAvailableLanguages()


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
    lang = str(portal.get_default_language()[:2])
    languages = get_available_languages_iso()
    if lang in languages:
        def_lang = languages[lang]
    else:
        def_lang = DEFAULT_LANGUAGE

    return def_lang


def get_current_language():
    lang = str(portal.get_current_language()[:2])
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


class LiteralHandler(object):
    """Handles Literal to I18Nfield conversion"""

    def __init__(self):
        self.available_languages = get_available_languages_iso()
        self.all_languages = get_available_languages_title().values()
        self.def_lang = get_default_language()

    def literal2dict(self, literal):
        res = {}
        lang = literal.language

        # convert 2-letter-format to 3-letter-format
        if str(lang) in self.available_languages:
            lang = self.available_languages[str(lang)]

        elif lang not in self.all_languages:
            lang = self.def_lang

        res[lang] = literal.value

        return res
