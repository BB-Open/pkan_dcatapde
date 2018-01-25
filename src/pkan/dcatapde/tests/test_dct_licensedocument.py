# -*- coding: utf-8 -*-

from pkan.dcatapde.content.dct_licensedocument import IDct_Licensedocument
from pkan.dcatapde import testing
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class Dct_LicensedocumentIntegrationTest(unittest.TestCase):

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='dct_licensedocument')
        schema = fti.lookupSchema()
        self.assertEqual(IDct_Licensedocument, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='dct_licensedocument')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='dct_licensedocument')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IDct_Licensedocument.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='dct_licensedocument',
            id='dct_licensedocument',
        )
        self.assertTrue(IDct_Licensedocument.providedBy(obj))
