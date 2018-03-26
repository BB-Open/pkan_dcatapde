# -*- coding: utf-8 -*-
from pkan.dcatapde.vocabularies import utils
from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class PortalCatalogVocabulary(object):
    """A vocabulary returning all objects from portal catalog."""

    def get_results(self, query):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(query)
        terms = []

        for brain in brains:
            obj = brain.getObject()
            if getattr(obj, 'title_for_vocabulary', None):
                terms.append(
                    SimpleTerm(
                        value=brain.UID,
                        token=str(brain.UID),
                        title=obj.title_for_vocabulary(),
                    ),
                )
            else:
                terms.append(
                    SimpleTerm(
                        value=brain.UID,
                        token=str(brain.UID),
                        title=obj.Title(),
                    ),
                )

        return SimpleVocabulary(terms)

    def __call__(self, context, query=None):
        query = utils.parse_query(context=context, query=query)
        return self.get_results(query=query)

PortalCatalogVocabularyFactory = PortalCatalogVocabulary()
