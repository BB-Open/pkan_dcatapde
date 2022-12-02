# -*- coding: utf-8 -*-
"""Content type tests for `dct_licensedocument`."""

import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.content.dct_rightsstatement import IDCTRightsStatement


class DCTRightsStatementIntegrationTest(unittest.TestCase):
    """Validate the `dct_rightststatemen` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_DCT_RIGHTSSTATEMENT,
        )
        schema = fti.lookupSchema()
        self.assertEqual(IDCTRightsStatement, schema)

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_DCT_RIGHTSSTATEMENT,
        )
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_DCT_RIGHTSSTATEMENT,
        )
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IDCTRightsStatement.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal.get(constants.FOLDER_RIGHTS),
            type=constants.CT_DCT_RIGHTSSTATEMENT,
            id='sample-license',
        )
        self.assertTrue(IDCTRightsStatement.providedBy(obj))
