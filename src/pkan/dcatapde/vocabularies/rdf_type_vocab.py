# -*- coding: utf-8 -*-
from pkan.dcatapde.harvesting.rdf import interfaces
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class RdfTypeVocabulary(object):
    """
    """

    def __call__(self, context):
        # create a list of SimpleTerm items:
        terms = []

        # Todo: Internationalize/move strings to constants.py
        # terms.append(
        #     SimpleTerm(
        #         value=interfaces.IJson,
        #         token='json',
        #         title='JSON generic',
        #     ),
        # )
        terms.append(
            SimpleTerm(
                value=interfaces.IRDFJSONLD,
                token='json-ld',
                title='RDF/JSON-LD',
            ),
        )
        terms.append(
            SimpleTerm(
                value=interfaces.IRDFXML,
                token='rdf-xml',
                title='RDF/XML',
            ),
        )
        terms.append(
            SimpleTerm(
                value=interfaces.IRDFTTL,
                token='rdf-ttl',
                title='RDF/Turtle',
            ),
        )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


RdfTypeVocabFactory = RdfTypeVocabulary()
