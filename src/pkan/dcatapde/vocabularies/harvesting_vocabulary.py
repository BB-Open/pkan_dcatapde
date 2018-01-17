# -*- coding: utf-8 -*-
from pkan.dcatapde.harvesting.interfaces import IJson
from pkan.dcatapde.harvesting.interfaces import IXml
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class HarvestingVocabulary(object):
    """
    """

    def __call__(self, context):
        # create a list of SimpleTerm items:
        terms = []

        terms.append(
            SimpleTerm(
                value=IJson, token='JSON', title='JSON'))
        terms.append(
            SimpleTerm(
                value=IXml, token='XML', title='XML'))
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


HarvestingVocabularyFactory = HarvestingVocabulary()
