# -*- coding: utf-8 -*-
"""Vocabularies and sources for content types."""
from operator import itemgetter

from plone import api
from plone.app.vocabularies.language import AvailableContentLanguageVocabulary
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class PKANLanguageVocabulary(AvailableContentLanguageVocabulary):

    def __call__(self, context, query=None):
        from Products.CMFPlone.utils import safe_unicode
        query = query or u''
        query = safe_unicode(query)
        items = [SimpleTerm('en', 'en', 'English')]  # default, only english
        ltool = api.portal.get_tool('portal_languages')
        if ltool is not None:
            languages = ltool.getAvailableLanguages()
            items = [
                (lg, languages[lg].get('native', lg)) for lg in languages
                if query.lower() in languages[lg].get('native', lg).lower()
            ]
            items.sort(key=itemgetter(1))
            items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)


PKANLanguageVocabularyFactory = PKANLanguageVocabulary()  # noqa
