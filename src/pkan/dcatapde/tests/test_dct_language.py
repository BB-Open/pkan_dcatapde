# -*- coding: utf-8 -*-
"""Content type tests for `dct_language`."""

import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.content.dct_language import IDCTLanguage


class DCTLanguageIntegrationTest(unittest.TestCase):
    """Validate the `dct_language` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_DCT_LANGUAGE,
        )
        schema = fti.lookupSchema()
        self.assertEqual(IDCTLanguage, schema)

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_DCT_LANGUAGE,
        )
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name=constants.CT_DCT_LANGUAGE,
        )
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IDCTLanguage.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal.get(constants.FOLDER_LANGUAGES),
            type=constants.CT_DCT_LANGUAGE,
            id='sample-language',
        )
        self.assertTrue(IDCTLanguage.providedBy(obj))
