# -*- coding: utf-8 -*-
"""Content type tests for `harvesterfolder`."""

from pkan.dcatapde import testing
from pkan.dcatapde.content.harvester_field_config import IHarvesterFieldConfig
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class HarvesterFieldConfigIntegrationTest(unittest.TestCase):
    """Validate the `harvester_field_config` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='harvester_field_config')
        schema = fti.lookupSchema()
        self.assertEqual(IHarvesterFieldConfig, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='harvester_field_config')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='harvester_field_config')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IHarvesterFieldConfig.providedBy(obj))

    # def test_adding(self):
    #     setRoles(self.portal, TEST_USER_ID, ['Contributor'])
    #     obj = api.content.create(
    #         container=self.portal,
    #         type='harvester_field_config',
    #         id='harvester_field_config',
    #     )
    #     self.assertTrue(IHarvesterFieldConfig.providedBy(obj))
