# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import CT_Harvester
from plone import api
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class SourceFieldVocabulary(object):
    """
    """

    def __call__(self, context):
        # TODO: given context is no context object. It is just the data of
        # the row in datagrid field
        # create a list of SimpleTerm items:
        terms = []

        request = getRequest()

        # index 0 is portal, so we do not need
        steps = request.steps[1:]

        context = api.portal.get()

        harvester = None

        for x in steps:
            context = context[x]
            if context.portal_type == CT_Harvester:
                harvester = context
                break

        if harvester:
            processor = harvester.type(harvester)
            fields = processor.read_fields()
            for field in fields:
                terms.append(
                    SimpleTerm(
                        value=field, token=field, title=field)
                )

        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


SourceFieldVocabularyFactory = SourceFieldVocabulary()
