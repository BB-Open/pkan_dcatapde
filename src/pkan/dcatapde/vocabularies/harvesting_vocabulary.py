# -*- coding: utf-8 -*-
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class HarvestingVocabulary(object):
    """
    """

    def __call__(self, context):
        # create a list of SimpleTerm items:
        terms = []

        # Todo: New Harvesting Types for new import

        # # Todo: Internationalize/move strings to constants.py
        # terms.append(
        #     SimpleTerm(
        #         value=i.IDefaultType,
        #         token='Default',
        #         title='Default',
        #     ),
        # )
        # # Todo: Implement
        # terms.append(
        #     SimpleTerm(
        #         value=i.ILicenseType,
        #         token='License',
        #         title='License',
        #     ),
        # )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


HarvestingVocabularyFactory = HarvestingVocabulary()
