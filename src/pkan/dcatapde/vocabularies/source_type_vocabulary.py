# -*- coding: utf-8 -*-
from pkan.dcatapde.harvesting.source_type import interfaces as i
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class SourceTypeVocabulary(object):
    """
    """

    def __call__(self, context):
        # create a list of SimpleTerm items:
        terms = []

        terms.append(
            SimpleTerm(
                value=i.IJson, token='Json', title='Json'))
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


SourceTypeVocabularyFactory = SourceTypeVocabulary()
