# -*- coding: utf-8 -*-
"""Content type tests for `dcat_catalog`."""

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.content.dcat_collectioncatalog import IDCATCollectionCatalog
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class CatalogIntegrationTest(unittest.TestCase):
    """Validate the `dcat_catalog` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI,
                           name=constants.CT_DCAT_COLLECTION_CATALOG)
        schema = fti.lookupSchema()
        self.assertEqual(IDCATCollectionCatalog, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI,
                           name=constants.CT_DCAT_COLLECTION_CATALOG)
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI,
                           name=constants.CT_DCAT_COLLECTION_CATALOG)
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IDCATCollectionCatalog.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_COLLECTION_CATALOG,
            id=constants.CT_DCAT_COLLECTION_CATALOG,
        )
        self.assertTrue(IDCATCollectionCatalog.providedBy(obj))
