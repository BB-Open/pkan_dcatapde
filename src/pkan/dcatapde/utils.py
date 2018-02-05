# -*- coding: utf-8 -*-
"""Utilities."""

from plone import api
from plone.i18n.locales.languages import _combinedlanguagelist
from plone.i18n.locales.languages import _languagelist
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
        l_tool = api.portal.get_tool('portal_languages')
        return l_tool.getSupportedLanguages()

    def getDefaultLanguage(self):
        """Return the system default language."""
        return api.portal.get_default_language()

    def getLanguages(self, combined=False):
        """Return a sequence of Language objects for available languages."""
        l_tool = api.portal.get_tool('portal_languages')
        return l_tool.getSupportedLanguages()

    def getLanguageListing(self, combined=False):
        """Return a sequence of language code and language name tuples."""
        languages = _languagelist.copy()
        if combined:
            languages.update(_combinedlanguagelist.copy())
        return [
            (code, u'{0} ({1})'.format(languages[code][u'name'], code))
            for code in languages
        ]


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
