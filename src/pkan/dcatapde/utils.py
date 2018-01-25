# -*- coding: utf-8 -*-
"""Utilities."""

from plone.i18n.locales.languages import _combinedlanguagelist
from plone.i18n.locales.languages import _languagelist
from ps.zope.i18nfield.interfaces import ILanguageAvailability
from ps.zope.i18nfield.plone import utils
from zope.interface import implementer


@implementer(ILanguageAvailability)
class LanguageAvailability(utils.LanguageAvailability):
    """Custom language availablility"""

    def getLanguageListing(self, combined=False):
        """Return a sequence of language code and language name tuples."""
        languages = _languagelist.copy()
        if combined:
            languages.update(_combinedlanguagelist.copy())
        return [
            (code, u'{0} ({1})'.format(languages[code][u'name'], code))
            for code in languages
        ]
