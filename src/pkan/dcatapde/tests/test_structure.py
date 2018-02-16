# -*- coding: utf-8 -*-
"""tests for `structure`."""

from pkan.dcatapde import testing
from pkan.dcatapde.structure import StructBase
from pkan.dcatapde.structure import StructDCATCatalog
from pkan.dcatapde.structure import StructDCATDataset
from pkan.dcatapde.structure import StructFOAFAgent
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class HarvesterIntegrationTest(unittest.TestCase):
    """Validate the `structure classes`."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_base_struct(self):
        base = StructBase()
        self.assertEqual(base.vocab_terms, [])

    def test_foaf_agent_struct(self):
        base = StructFOAFAgent()
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dcat_catalog_struct(self):
        base = StructDCATCatalog()
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dcat_dataset_struct(self):
        base = StructDCATDataset()
        self.assertGreater(len(base.vocab_terms), 0)
