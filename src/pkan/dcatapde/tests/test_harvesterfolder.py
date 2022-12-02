# -*- coding: utf-8 -*-
"""Content type tests for `harvesterfolder`."""

import unittest

from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.content.harvesterfolder import IHarvesterfolder


class HarvesterfolderIntegrationTest(unittest.TestCase):
    """Validate the `harvesterfolder` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_HARVESTER_FOLDER)
        schema = fti.lookupSchema()
        self.assertEqual(IHarvesterfolder, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_HARVESTER_FOLDER)
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_HARVESTER_FOLDER)
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IHarvesterfolder.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type=constants.CT_HARVESTER_FOLDER,
            id=constants.CT_HARVESTER_FOLDER,
        )
        self.assertTrue(IHarvesterfolder.providedBy(obj))
