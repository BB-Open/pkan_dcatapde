# -*- coding: utf-8 -*-
"""Pre-processor vocabularies."""

from pkan.dcatapde.harvesting.data_type.interfaces import IPotsdam
from pkan.dcatapde.harvesting.data_type.interfaces import IRDF
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class DataTypeVocabulary(object):
    """Pre-processor vocabulary."""

    def __call__(self, context):
        # create a list of SimpleTerm items:
        terms = []

        # Todo: Internationalize/move strings to constants.py
        terms.append(
            SimpleTerm(
                value=IRDF,
                token='rdf',
                title='RDF'),
        )
        terms.append(
            SimpleTerm(
                value=IPotsdam,
                token='Potsdam',
                title='Potsdam'),
        )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


DataTypeVocabularyFactory = DataTypeVocabulary()
