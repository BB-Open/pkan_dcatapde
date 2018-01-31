# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import CT_FOAF_AGENT
from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class FOAFagentVocabulary(object):
    """
    """

    def __call__(self, context):
        brains = api.content.find(portal_type=CT_FOAF_AGENT)

        # create a list of SimpleTerm items:
        terms = []
        for brain in brains:
            obj = brain.getObject()
            url = obj.absolute_url()
            terms.append(
                SimpleTerm(
                    value=brain.UID, token=str(brain.UID), title=url))
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


FoafagentVocabularyFactory = FOAFagentVocabulary()
