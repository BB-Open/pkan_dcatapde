# -*- coding: utf-8 -*-
"""DCAT field vocabularies."""
from pkan.dcatapde import constants
from pkan.dcatapde.api.functions import get_ancestor
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IContextSourceBinder)
class DcatFieldVocabulary(object):
    """DKAT field vocabulary."""

    def __call__(self, context):
        terms = []

        harvester = get_ancestor(context, constants.CT_HARVESTER)

        if harvester:
            processor = harvester.source_type(harvester)
            terms = processor.read_dcat_fields()

        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)
