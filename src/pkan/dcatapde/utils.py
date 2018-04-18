# -*- coding: utf-8 -*-
"""Utilities."""
from pkan.dcatapde.languages import AVAILABLE_LANGUAGES_ISO
from pkan.dcatapde.languages import AVAILABLE_LANGUAGES_TITLE
from pkan.dcatapde.languages import DEFAULT_LANGUAGE
from plone.api import portal
from ps.zope.i18nfield.interfaces import ILanguageAvailability
from ps.zope.i18nfield.plone.utils import LanguageAvailability
from zope.annotation.interfaces import IAnnotations
from zope.globalrequest import getRequest
from zope.interface import implementer


@implementer(ILanguageAvailability)
class PKANLanguages(LanguageAvailability):
    """A list of available languages."""

    def getAvailableLanguages(self, combined=False):
        """Return a sequence of language tags for available languages."""
        res = AVAILABLE_LANGUAGES_TITLE.keys()
        return res

    def getDefaultLanguage(self):
        """Return the system default language."""
        res = unicode(super(PKANLanguages, self).getDefaultLanguage())
        if res in AVAILABLE_LANGUAGES_ISO:
            return AVAILABLE_LANGUAGES_ISO[unicode(res)]
        else:
            return DEFAULT_LANGUAGE

    def getLanguages(self, combined=False):
        """Return a sequence of Language objects for available languages."""
        res = {}

        for lang in AVAILABLE_LANGUAGES_TITLE.keys():
            res[lang] = {u'name': AVAILABLE_LANGUAGES_TITLE[lang]}

        return res

    def getLanguageListing(self, combined=False):
        """Return a sequence of language code and language name tuples."""
        res = []
        for lang in AVAILABLE_LANGUAGES_TITLE.keys():
            res.append((lang, AVAILABLE_LANGUAGES_TITLE[lang]))
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
    if lang in AVAILABLE_LANGUAGES_ISO:
        def_lang = AVAILABLE_LANGUAGES_ISO[lang]
    else:
        def_lang = DEFAULT_LANGUAGE

    return def_lang


def get_current_language():
    lang = unicode(portal.get_current_language()[:2])
    if lang in AVAILABLE_LANGUAGES_ISO:
        cur_lang = AVAILABLE_LANGUAGES_ISO[lang]
    else:
        cur_lang = DEFAULT_LANGUAGE

    return cur_lang
