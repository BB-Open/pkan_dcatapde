# -*- coding: utf-8 -*-
"""Content type tests for `distribution`."""

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.content.dcat_distribution import IDCATDistribution
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class DistributionIntegrationTest(unittest.TestCase):
    """Validate the `distribution` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.cat = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_CATALOG,
            id='catalog-1',
            dct_title={u'en': u'Catalog 1'},
        )
        self.dataset = api.content.create(
            container=self.cat,
            type=constants.CT_DCAT_DATASET,
            id=constants.CT_DCAT_DATASET,
        )

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_DCAT_DISTRIBUTION)
        schema = fti.lookupSchema()
        self.assertEqual(IDCATDistribution, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_DCAT_DISTRIBUTION)
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name=constants.CT_DCAT_DISTRIBUTION)
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IDCATDistribution.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.dataset,
            type=constants.CT_DCAT_DISTRIBUTION,
            id=constants.CT_DCAT_DISTRIBUTION,
        )
        self.assertTrue(IDCATDistribution.providedBy(obj))
