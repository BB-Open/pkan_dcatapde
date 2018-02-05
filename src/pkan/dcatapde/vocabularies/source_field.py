# -*- coding: utf-8 -*-
"""Source field vocabularies."""
from pkan.dcatapde import constants
from pkan.dcatapde.api.functions import get_ancestor
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IContextSourceBinder)
class SourceFieldVocabulary(object):
    """Source field vocabulary."""

    def __call__(self, context):
        terms = []

        harvester = get_ancestor(context, constants.CT_HARVESTER)

        if harvester:
            processor = harvester.source_type(harvester)
            fields = processor.read_fields()
            for field in fields:
                terms.append(
                    SimpleTerm(value=field, token=field, title=field),
                )

        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)
