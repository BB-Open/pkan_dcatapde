# -*- coding: utf-8 -*-
from pkan.dcatapde.content.literal import ILiteral
from pkan.dcatapde.testing import PKAN_DCATAPDE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class LiteralIntegrationTest(unittest.TestCase):

    layer = PKAN_DCATAPDE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='literal')
        schema = fti.lookupSchema()
        self.assertEqual(ILiteral, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='literal')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='literal')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(ILiteral.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='literal',
            id='literal',
        )
        self.assertTrue(ILiteral.providedBy(obj))
