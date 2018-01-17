# -*- coding: utf-8 -*-
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.testing import PKAN_DCATAPDE_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class HarvesterIntegrationTest(unittest.TestCase):

    layer = PKAN_DCATAPDE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='harvester')
        schema = fti.lookupSchema()
        self.assertEqual(IHarvester, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='harvester')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='harvester')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IHarvester.providedBy(obj))

    # def test_adding(self):
    #     setRoles(self.portal, TEST_USER_ID, ['Contributor'])
    #     obj = api.content.create(
    #         container=self.portal,
    #         type='harvester',
    #         id='harvester',
    #     )
    #     self.assertTrue(IHarvester.providedBy(obj))
