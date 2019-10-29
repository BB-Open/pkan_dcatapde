# -*- coding: utf-8 -*-

from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


HARVEST_PLONE = 'Plone'
HARVEST_TRIPELSTORE = 'Tripelstore'


@implementer(IVocabularyFactory)
class HarvesterTargetVocabulary(object):
    """
    """

    def __call__(self, context):
        # create a list of SimpleTerm items:
        terms = []

        terms.append(
            SimpleTerm(
                value=HARVEST_PLONE,
                token=HARVEST_PLONE,
                title='Plone',
            ),
        )
        terms.append(
            SimpleTerm(
                value=HARVEST_TRIPELSTORE,
                token=HARVEST_TRIPELSTORE,
                title='Tripel Store',
            ),
        )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


HarvesterTargetVocabFactory = HarvesterTargetVocabulary()
