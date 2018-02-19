# -*- coding: utf-8 -*-
"""DCAT field vocabularies."""
from pkan.dcatapde.constants import DCAT_CTs
from pkan.dcatapde.structure.structure import IStructure
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getUtility
from zope.dottedname.resolve import resolve
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IContextSourceBinder)
class DcatFieldVocabulary(object):
    """DCAT field vocabulary."""

    def __init__(self, cts=None):
        # parameter can be used to reduce number of cts
        if cts:
            self.cts = cts
        else:
            self.cts = DCAT_CTs

    def __call__(self, context):
        # if (context is None or
        #         isinstance(context, dict) or
        #         'NO_VALUE' in str(context)):
        #     context = utils.get_request_annotations(
        #         'pkan.vocabularies.context',
        #     )
        terms = []

        for ct in self.cts:
            klass = resolve(getUtility(IDexterityFTI, name=ct).klass)

            # just an adaptable test instance without properties to get adapter
            klass_instance = klass()

            try:
                structure_adapter = IStructure(klass_instance)
            except TypeError:
                continue
            terms += structure_adapter.vocab_terms

        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)
