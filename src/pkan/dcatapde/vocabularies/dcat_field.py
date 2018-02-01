# -*- coding: utf-8 -*-
"""DCAT field vocabularies."""
from pkan.dcatapde.constants import CT_HARVESTER
from plone import api
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class DcatFieldVocabulary(object):
    """DKAT field vocabulary."""

    def __call__(self, context):
        terms = []
        request = getRequest()

        # index 0 is portal, so we do not need
        steps = request.steps[1:]

        context = api.portal.get()

        harvester = None

        for x in steps:
            context = context[x]
            if context.portal_type == CT_HARVESTER:
                harvester = context
                break

        if harvester:
            processor = harvester.source_type(harvester)
            terms = processor.read_dcat_fields()

        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


DcatFieldVocabularyFactory = DcatFieldVocabulary()
