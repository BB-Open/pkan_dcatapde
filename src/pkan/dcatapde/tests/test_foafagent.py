# -*- coding: utf-8 -*-
"""Content type tests for `foafagent`."""

from pkan.dcatapde import testing
from pkan.dcatapde.content.foafagent import IFoafagent
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class FoafagentIntegrationTest(unittest.TestCase):
    """Validate the `foafagent` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='foafagent')
        schema = fti.lookupSchema()
        self.assertEqual(IFoafagent, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='foafagent')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='foafagent')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IFoafagent.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='foafagent',
            id='foafagent',
        )
        self.assertTrue(IFoafagent.providedBy(obj))
