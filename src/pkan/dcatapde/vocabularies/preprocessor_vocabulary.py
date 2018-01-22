# -*- coding: utf-8 -*-
from pkan.dcatapde.harvesting.prep_interfaces import IPotsdam
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class PreprocessorVocabulary(object):
    """
    """

    def __call__(self, context):
        # create a list of SimpleTerm items:
        terms = []

        terms.append(
            SimpleTerm(
                value=IPotsdam, token='Potsdam', title='Potsdam'))
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


PreprocessorVocabularyFactory = PreprocessorVocabulary()
