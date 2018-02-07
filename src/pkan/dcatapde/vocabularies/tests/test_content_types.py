# -*- coding: utf-8 -*-
"""Test license document related vocabularies."""

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized

import unittest


class TestDCATCatalogVocabulary(unittest.TestCase):
    """Validate the `DCATCatalogVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_CATALOG,
            id='catalog-1',
            dct_title={u'en': u'Catalog 1'},
        )
        self.item2 = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_CATALOG,
            id='catalog-2',
            dct_title={u'en': u'Catalog 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.DCATCatalog'
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(len(vocabulary), 2)
        self.assertEqual(
            vocabulary.getTerm(self.item1.UID()).title,
            self.item1.Title(),
        )
        self.assertEqual(
            vocabulary.getTerm(self.item2.UID()).title,
            self.item2.Title(),
        )


class TestDCATDatasetVocabulary(unittest.TestCase):
    """Validate the `DCATDatasetVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_DATASET,
            id='dataset-1',
            dct_title={u'en': u'Dataset 1'},
        )
        self.item2 = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_DATASET,
            id='dataset-2',
            dct_title={u'en': u'Dataset 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.DCATDataset'
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(len(vocabulary), 2)
        self.assertEqual(
            vocabulary.getTerm(self.item1.UID()).title,
            self.item1.Title(),
        )
        self.assertEqual(
            vocabulary.getTerm(self.item2.UID()).title,
            self.item2.Title(),
        )


class TestDCATDistributionVocabulary(unittest.TestCase):
    """Validate the `DCATDistributionVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_DISTRIBUTION,
            id='distribution-1',
            dct_title={u'en': u'Distribution 1'},
        )
        self.item2 = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_DISTRIBUTION,
            id='distribution-2',
            dct_title={u'en': u'Distribution 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.DCATDistribution'
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(len(vocabulary), 2)
        self.assertEqual(
            vocabulary.getTerm(self.item1.UID()).title,
            self.item1.Title(),
        )
        self.assertEqual(
            vocabulary.getTerm(self.item2.UID()).title,
            self.item2.Title(),
        )


class TestDCTLicenseDocumentVocabulary(unittest.TestCase):
    """Validate the `DCTLicenseDocumentVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal.get(constants.FOLDER_LICENSES),
            type=constants.CT_DCT_LICENSEDOCUMENT,
            id='license-1',
            dct_title={u'en': u'License 1'},
            rdfs_isDefinedBy='https://example.com/license-1',
        )
        self.item2 = api.content.create(
            container=self.portal.get(constants.FOLDER_LICENSES),
            type=constants.CT_DCT_LICENSEDOCUMENT,
            id='license-2',
            dct_title={u'en': u'License 2'},
            rdfs_isDefinedBy='https://example.com/license-2',
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.DCTLicenseDocument'
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(len(vocabulary), 2)
        self.assertEqual(
            vocabulary.getTerm(self.item1.UID()).title,
            '{0} ({1})'.format(
                self.item1.Title(),
                self.item1.rdfs_isDefinedBy,
            ),
        )
        self.assertEqual(
            vocabulary.getTerm(self.item2.UID()).title,
            '{0} ({1})'.format(
                self.item2.Title(),
                self.item2.rdfs_isDefinedBy,
            ),
        )
