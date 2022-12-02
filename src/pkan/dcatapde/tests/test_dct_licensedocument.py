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
from pkan.dcatapde.content.dct_licensedocument import IDCTLicenseDocument


class DCTLicenseDocumentIntegrationTest(unittest.TestCase):
    """Validate the `dct_licensedocument` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_DCT_LICENSEDOCUMENT,
        )
        schema = fti.lookupSchema()
        self.assertEqual(IDCTLicenseDocument, schema)

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_DCT_LICENSEDOCUMENT,
        )
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_DCT_LICENSEDOCUMENT,
        )
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IDCTLicenseDocument.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal.get(constants.FOLDER_LICENSES),
            type=constants.CT_DCT_LICENSEDOCUMENT,
            id='sample-license',
        )
        self.assertTrue(IDCTLicenseDocument.providedBy(obj))
