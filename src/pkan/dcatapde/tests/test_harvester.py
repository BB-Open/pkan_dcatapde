# -*- coding: utf-8 -*-
"""Content type tests for `harvester`."""

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.content.harvester import IHarvester
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class HarvesterIntegrationTest(unittest.TestCase):
    """Validate the `harvester` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_HARVESTER)
        schema = fti.lookupSchema()
        self.assertEqual(IHarvester, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_HARVESTER)
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_HARVESTER)
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IHarvester.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        folder = api.content.create(
            container=self.portal,
            type=constants.CT_HARVESTER_FOLDER,
            id=constants.CT_HARVESTER_FOLDER,
        )
        obj = api.content.create(
            container=folder,
            type=constants.CT_HARVESTER,
            id=constants.CT_HARVESTER,
        )
        self.assertTrue(IHarvester.providedBy(obj))
