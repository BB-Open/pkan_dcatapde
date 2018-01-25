# -*- coding: utf-8 -*-
from pkan.dcatapde.content.dct_mediatypeorextent import IDct_Mediatypeorextent
from pkan.dcatapde.testing import PKAN_DCATAPDE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class Dct_MediatypeorextentIntegrationTest(unittest.TestCase):

    layer = PKAN_DCATAPDE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='dct_mediatypeorextent')
        schema = fti.lookupSchema()
        self.assertEqual(IDct_Mediatypeorextent, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='dct_mediatypeorextent')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='dct_mediatypeorextent')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IDct_Mediatypeorextent.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='dct_mediatypeorextent',
            id='dct_mediatypeorextent',
        )
        self.assertTrue(IDct_Mediatypeorextent.providedBy(obj))
