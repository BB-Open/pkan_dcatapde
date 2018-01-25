# -*- coding: utf-8 -*-
"""DCAT field vocabularies."""
from pkan.dcatapde.api.functions import get_terms_for_ct
from pkan.dcatapde.constants import DCAT_CTs
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class DcatFieldVocabulary(object):
    """DKAT field vocabulary."""

    def __call__(self, context):
        terms = []
        for CT in DCAT_CTs:
            terms = terms + get_terms_for_ct(CT)

        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


DcatFieldVocabularyFactory = DcatFieldVocabulary()
