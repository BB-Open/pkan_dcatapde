# -*- coding: utf-8 -*-
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

        # TODO: just dummy data at the moment, need to be replaced
        terms.append(
            SimpleTerm(
                value='JSON', token='JSON', title='JSON'))
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


HarvestingVocabularyFactory = HarvestingVocabulary()
