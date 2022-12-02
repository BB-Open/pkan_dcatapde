# -*- coding: utf-8 -*-
"""Content type tests for `foafagent`."""

import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.content.foaf_agent import IFOAFAgent


class FoafagentIntegrationTest(unittest.TestCase):
    """Validate the `foafagent` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.folder = self.portal.get(constants.FOLDER_AGENTS)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_FOAF_AGENT)
        schema = fti.lookupSchema()
        self.assertEqual(IFOAFAgent, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_FOAF_AGENT)
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_FOAF_AGENT)
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IFOAFAgent.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.folder,
            type=constants.CT_FOAF_AGENT,
            id=constants.CT_FOAF_AGENT,
        )
        self.assertTrue(IFOAFAgent.providedBy(obj))
        obj.reindexObject()
