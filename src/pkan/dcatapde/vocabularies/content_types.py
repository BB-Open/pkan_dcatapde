# -*- coding: utf-8 -*-
"""Vocabularies and sources for content types."""

from pkan.dcatapde import constants
from pkan.dcatapde.vocabularies import utils
from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class BaseContentTypeVocabulary(object):
    """A vocabulary returning a list of objects from a content type."""

    portal_type = None

    def get_results(self, query):
        params = {
            'portal_type': self.portal_type,
        }
        query.update(params)

        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(query)
        terms = []

        for brain in brains:
            obj = brain.getObject()
            terms.append(
                SimpleTerm(
                    value=brain.UID,
                    token=str(brain.UID),
                    title=obj.title_for_vocabulary(),
                ),
            )

        return SimpleVocabulary(terms)

    def __call__(self, context, query=None):
        query = utils.parse_query(context=context, query=query)
        return self.get_results(query=query)


@implementer(IVocabularyFactory)
class DCTLicenseDocumentVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning DCTLicenseDocuments."""

    portal_type = constants.CT_DCT_LICENSEDOCUMENT


DCTLicenseDocumentVocabularyFactory = DCTLicenseDocumentVocabulary()
