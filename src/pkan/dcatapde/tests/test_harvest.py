# -*- coding: utf-8 -*-
"""Content type tests for `harvester`."""
import unittest

import requests
from pkan.dcatapde.harvesting.manager import interfaces
from pkan.dcatapde.harvesting.load_data.visitors import DCATVisitor
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.browser.content_views.harvester import RDFProcessor_factory
from pkan.dcatapde.content.harvester import IHarvester

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
            source_type=interfaces.IRDFTTL,
        )
        self.assertTrue(IHarvester.providedBy(self.obj))

    def testHarvestTripelstore(self):
        req = requests.get(FIXTURE_URL)
        self.assertEqual(req.status_code, 200)

        rdfproc = RDFProcessor_factory(self.obj)

        visitor = DCATVisitor()
        visitor.real_run = False
        rdfproc.prepare_and_run(visitor)

        visitor.real_run = True
        rdfproc.prepare_and_run(visitor)
