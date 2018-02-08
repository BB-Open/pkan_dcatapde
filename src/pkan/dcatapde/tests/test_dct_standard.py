# -*- coding: utf-8 -*-
"""Content type tests for `dct_standard`."""

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.content.dct_standard import IDCTStandard
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class DCTStandardIntegrationTest(unittest.TestCase):
    """Validate the `dct_standard` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_DCT_STANDARD,
        )
        schema = fti.lookupSchema()
        self.assertEqual(IDCTStandard, schema)

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_DCT_STANDARD,
        )
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_DCT_STANDARD,
        )
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IDCTStandard.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal.get(constants.FOLDER_STANDARDS),
            type=constants.CT_DCT_STANDARD,
            id='sample-standard',
        )
        self.assertTrue(IDCTStandard.providedBy(obj))
