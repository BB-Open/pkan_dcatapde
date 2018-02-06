# -*- coding: utf-8 -*-
"""Vocabulary tests for `FOAFAgent`."""

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized

import unittest


class FoafagentVocabularyIntegrationTest(unittest.TestCase):
    """Validate the `FOAFAgent` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.n1 = api.content.create(
            type=constants.CT_FOAF_AGENT, title='N1', container=self.portal)
        self.n2 = api.content.create(
            type=constants.CT_FOAF_AGENT, title='N2', container=self.portal)

    def test_vocabulary(self):
        vocab_name = 'pkan.dcatapde.FOAFagentVocabulary'
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(
            vocabulary.getTerm(self.n1.UID()).title,
            self.n1.absolute_url())
        self.assertEqual(
            vocabulary.getTerm(self.n2.UID()).title,
            self.n2.absolute_url())