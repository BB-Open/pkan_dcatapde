# -*- coding: utf-8 -*-
"""Content type tests for `harvester`."""
from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.browser.content_views.harvester import RDFProcessor_factory
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.rdf import interfaces
from pkan.dcatapde.vocabularies.harvester_target import HARVEST_PLONE
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import requests
import unittest


FIXTURE_URL = 'https://raw.githubusercontent.com/BB-Open/pkan.dcatapde/master/src/pkan/dcatapde/tests/fixtures/potsdam.ttl'  # noqa: E501


class HarvestTest(unittest.TestCase):
    """Validate the `harvester` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        folder = api.content.create(
            container=self.portal,
            type=constants.CT_HARVESTER_FOLDER,
            id=constants.CT_HARVESTER_FOLDER,
        )
        self.obj = api.content.create(
            container=folder,
            type=constants.CT_HARVESTER,
            id=constants.CT_HARVESTER,
            url=FIXTURE_URL,
            target=HARVEST_PLONE,
            source_type=interfaces.IRDFTTL,
            top_node=CT_DCAT_CATALOG,
        )
        self.assertTrue(IHarvester.providedBy(self.obj))

    def testHarvest(self):
        req = requests.get(FIXTURE_URL)
        self.assertEqual(req.status_code, 200)

        rdfproc = RDFProcessor_factory(self.obj, raise_exceptions=True)

        self.log = rdfproc.real_run()
