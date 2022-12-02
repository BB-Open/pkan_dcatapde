# -*- coding: utf-8 -*-

import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.content.vcard_kind import IVCARDKind


class VcardKindIntegrationTest(unittest.TestCase):
    """Validate the `dct_location` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_VCARD_KIND,
        )
        schema = fti.lookupSchema()
        self.assertEqual(IVCARDKind, schema)

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_VCARD_KIND,
        )
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_VCARD_KIND,
        )
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IVCARDKind.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal.get(constants.FOLDER_VCARD_KIND),
            type=constants.CT_VCARD_KIND,
            id='sample-location',
        )
        self.assertTrue(IVCARDKind.providedBy(obj))
