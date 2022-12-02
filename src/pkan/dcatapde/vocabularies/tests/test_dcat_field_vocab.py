# -*- coding: utf-8 -*-
"""Test Dcat Field Vocabulary."""

import unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.schema.interfaces import IVocabularyTokenized

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.vocabularies.dcat_field import DcatFieldVocabulary


class TestDcatFieldVocabulary(unittest.TestCase):
    """Validate the `DcatFieldVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_vocabulary_standard(self):
        """Validate the vocabulary."""
        vocab = DcatFieldVocabulary()

        vocabulary = vocab(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertTrue(len(vocabulary) > 0)

        # test that if we do not use all DCAT-Types,
        # we get a shorter Vocabulary
        vocab_catalog_only = DcatFieldVocabulary([constants.CT_DCAT_CATALOG])
        vocabulary_catalog_only = vocab_catalog_only(self.portal)

        self.assertTrue(len(vocabulary) > len(vocabulary_catalog_only))

    def test_vocabulary_no_cts(self):
        vocab = DcatFieldVocabulary([])

        vocabulary = vocab(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(len(vocabulary), 0)

    def test_vocabulary_wrong_cts(self):
        vocab = DcatFieldVocabulary([constants.CT_HARVESTER])

        vocabulary = vocab(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(len(vocabulary), 0)

    def test_vocabulary_unexistend_cts(self):
        vocab = DcatFieldVocabulary(['hello_world'])

        vocabulary = vocab(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(len(vocabulary), 0)
