# -*- coding: utf-8 -*-
"""Vocabularies and sources for content types."""
from operator import itemgetter
from plone.app.vocabularies.language import AvailableContentLanguageVocabulary
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
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
        site = getSite()
        ltool = getToolByName(site, 'portal_languages', None)
        if ltool is not None:
            languages = ltool.getAvailableLanguages()
            items = [
                (l, languages[l].get('native', l)) for l in languages
                if query.lower() in languages[l].get('native', l).lower()
            ]
            items.sort(key=itemgetter(1))
            items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)


PKANLanguageVocabularyFactory = PKANLanguageVocabulary()  # noqa
