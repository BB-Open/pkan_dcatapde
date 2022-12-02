# -*- coding: utf-8 -*-
import pkan_config.config as pkan_cfg
from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from pkan.dcatapde.constants import COMPLETE_SUFFIX


@implementer(IVocabularyFactory)
class DefaultStoresVocabulary(object):
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
        cfg = pkan_cfg.get_config()

        DEFAULT_STORES = [
            cfg.PLONE_SKOS_CONCEPT_NAMESPACE,
            cfg.PLONE_DCAT_NAMESPACE,
            cfg.PLONE_ALL_OBJECTS_NAMESPACE,
            cfg.PLONE_OWL_STORE,
        ]
        for store in DEFAULT_STORES:
            terms.append(
                SimpleTerm(
                    value=store,
                    token=store,
                    title=store,
                ),
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


DefaultStoresVocabFactory = DefaultStoresVocabulary()


@implementer(IVocabularyFactory)
class AllStoresVocabulary(object):
    """
    """

    def __call__(self, context):
        # create a list of SimpleTerm items:
        terms = []

        catalog = api.portal.get_tool('portal_catalog')
        vals = catalog._catalog.indexes['stores'].uniqueValues()

        cfg = pkan_cfg.get_config()

        DEFAULT_STORES = [
            cfg.PLONE_SKOS_CONCEPT_NAMESPACE,
            cfg.PLONE_DCAT_NAMESPACE,
            cfg.PLONE_ALL_OBJECTS_NAMESPACE,
            cfg.PLONE_OWL_STORE,
        ]

        for store in vals:
            if store in DEFAULT_STORES:
                continue
            terms.append(
                SimpleTerm(
                    value=store,
                    token=store,
                    title=store,
                ),
            )
            terms.append(
                SimpleTerm(
                    value=store + COMPLETE_SUFFIX,
                    token=store + COMPLETE_SUFFIX,
                    title=store + COMPLETE_SUFFIX,
                ),
            )
        for store in DEFAULT_STORES:
            terms.append(
                SimpleTerm(
                    value=store,
                    token=store,
                    title=store,
                ),
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


AllStoresVocabFactory = AllStoresVocabulary()
