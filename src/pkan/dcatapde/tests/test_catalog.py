# -*- coding: utf-8 -*-

from pkan.dcatapde.content.catalog import ICatalog
from pkan.dcatapde import testing
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class CatalogIntegrationTest(unittest.TestCase):

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='catalog')
        schema = fti.lookupSchema()
        self.assertEqual(ICatalog, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='catalog')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='catalog')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(ICatalog.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='catalog',
            id='catalog',
        )
        self.assertTrue(ICatalog.providedBy(obj))
