# -*- coding: utf-8 -*-
"""Content type tests for `dct_mediatypeorextent`."""

from pkan.dcatapde import testing
from pkan.dcatapde.content.dct_mediatypeorextent import IDct_Mediatypeorextent
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class DctMediatypeorextentIntegrationTest(unittest.TestCase):
    """Validate the `dct_mediatypeorextent` CT."""

    layer = testing.INTEGRATION_TESTING

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
