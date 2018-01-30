# -*- coding: utf-8 -*-
"""Content type tests for `dcat_dataset`."""

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.content.dcat_dataset import IDCATDataset
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class DatasetIntegrationTest(unittest.TestCase):
    """Validate the `dcat_dataset` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_DCAT_DATASET)
        schema = fti.lookupSchema()
        self.assertEqual(IDCATDataset, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_DCAT_DATASET)
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_DCAT_DATASET)
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IDCATDataset.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_DATASET,
            id=constants.CT_DCAT_DATASET,
        )
        self.assertTrue(IDCATDataset.providedBy(obj))
