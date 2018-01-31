# -*- coding: utf-8 -*-
"""Vocabularies and sources for license documents."""

from pkan.dcatapde.constants import CT_DCT_LICENSE_DOCUMENT
from plone import api
from plone.app.vocabularies.utils import parseQueryString
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class LicenseDocumentVocabulary(object):
    """A vocabulary returning license documents."""

    def licenses(self, query):
        params = {
            'portal_type': CT_DCT_LICENSE_DOCUMENT,
        }
        query.update(params)

        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(query)
        terms = []

        for brain in brains:
            obj = brain.getObject()
            title = u'{title} ({url})'.format(
                title=brain.Title,
                url=obj.rdf_about,
            )
            terms.append(
                SimpleTerm(
                    value=brain.UID,
                    token=str(brain.UID),
                    title=title,
                ),
            )

        return SimpleVocabulary(terms)

    def __call__(self, context, query=None):
        parsed = {}
        if query:
            if isinstance(query, basestring):
                q = query
                if not q.endswith('*'):
                    q = '{0}*'.format(q)
                query = {
                    'criteria': [{
                        'i': 'SearchableText',
                        'o': 'plone.app.querystring.operation.string.contains',
                        'v': q,
                    }],
                }
            parsed = parseQueryString(context, query['criteria'])
            if 'sort_on' in query:
                parsed['sort_on'] = query['sort_on']
            if 'sort_order' in query:
                parsed['sort_order'] = str(query['sort_order'])
        return self.licenses(query=parsed)


LicenseDocumentVocabularyFactory = LicenseDocumentVocabulary()
