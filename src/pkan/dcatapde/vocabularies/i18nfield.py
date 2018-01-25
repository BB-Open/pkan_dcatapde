from plone import api
from plone.api.portal import get_tool
from plone.i18n.locales.languages import _combinedlanguagelist
from plone.i18n.locales.languages import _languagelist
from ps.zope.i18nfield.interfaces import ILanguageAvailability
from ps.zope.i18nfield.plone.utils import LanguageAvailability
from zope.interface import implementer


@implementer(ILanguageAvailability)
class PKANLanguages(LanguageAvailability):
    """A list of available languages."""

    def getAvailableLanguages(self, combined=False):
        """Return a sequence of language tags for available languages."""
        languages = get_tool('portal_languages').getSupportedLanguages()
        return languages

    def getDefaultLanguage(self):
        """Return the system default language."""
        return api.portal.get_default_language()

    def getLanguages(self, combined=False):
        """Return a sequence of Language objects for available languages."""
        languages = get_tool('portal_languages').getSupportedLanguages()
        return languages

    def getLanguageListing(self, combined=False):
        """Return a sequence of language code and language name tuples."""
        languages = _languagelist.copy()
        if combined:
            languages.update(_combinedlanguagelist.copy())
        return [(code, languages[code][u'name']) for code in languages]
