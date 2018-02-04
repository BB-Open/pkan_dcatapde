# -*- coding: utf-8 -*-
"""Vocabularies and sources for license documents."""

from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.vocabularies import utils
from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class LicenseDocumentVocabulary(object):
    """A vocabulary returning license documents."""

    def licenses(self, query):
        params = {
            'portal_type': CT_DCT_LICENSEDOCUMENT,
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
        query = utils.parse_query(context=context, query=query)
        return self.licenses(query=query)


LicenseDocumentVocabularyFactory = LicenseDocumentVocabulary()
