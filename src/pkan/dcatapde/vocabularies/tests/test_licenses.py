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


class TestDCTLicenseDocumentVocabulary(unittest.TestCase):
    """Validate the `DCTLicenseDocumentVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.l1 = api.content.create(
            container=self.portal.get(constants.FOLDER_LICENSES),
            type=constants.CT_DCT_LICENSEDOCUMENT,
            id='license-1',
            dct_title={u'en': u'License 1'},
            rdfs_isDefinedBy='https://example.com/license-1',
        )
        self.l2 = api.content.create(
            container=self.portal.get(constants.FOLDER_LICENSES),
            type=constants.CT_DCT_LICENSEDOCUMENT,
            id='license-2',
            dct_title={u'en': u'License 2'},
            rdfs_isDefinedBy='https://example.com/license-2',
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.DCTLicenseDocuments'
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(len(vocabulary), 2)
        self.assertEqual(
            vocabulary.getTerm(self.l1.UID()).title,
            '{0} ({1})'.format(self.l1.Title(), self.l1.rdfs_isDefinedBy),
        )
        self.assertEqual(
            vocabulary.getTerm(self.l2.UID()).title,
            '{0} ({1})'.format(self.l2.Title(), self.l2.rdfs_isDefinedBy),
        )
