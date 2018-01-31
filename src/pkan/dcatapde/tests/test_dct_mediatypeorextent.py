# -*- coding: utf-8 -*-
"""Content type tests for `dct_mediatypeorextent`."""

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.content.dct_mediatypeorextent import IDCTMediatypeorextent
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
        fti = queryUtility(IDexterityFTI,
                           name=constants.CT_DCT_MEDIATYPEOREXTENT)
        schema = fti.lookupSchema()
        self.assertEqual(IDCTMediatypeorextent, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI,
                           name=constants.CT_DCT_MEDIATYPEOREXTENT)
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI,
                           name=constants.CT_DCT_MEDIATYPEOREXTENT)
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IDCTMediatypeorextent.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type=constants.CT_DCT_MEDIATYPEOREXTENT,
            id=constants.CT_DCT_MEDIATYPEOREXTENT,
        )
        self.assertTrue(IDCTMediatypeorextent.providedBy(obj))
