# -*- coding: utf-8 -*-
"""tests for `structure`."""

from pkan.dcatapde import testing
from pkan.dcatapde.structure.structure import StructBase
from pkan.dcatapde.structure.structure import StructDCATCatalog
from pkan.dcatapde.structure.structure import StructDCATDataset
from pkan.dcatapde.structure.structure import StructDCATDistribution
from pkan.dcatapde.structure.structure import StructDCTLicenseDocument
from pkan.dcatapde.structure.structure import StructDCTLocation
from pkan.dcatapde.structure.structure import StructDCTMediaTypeOrExtent
from pkan.dcatapde.structure.structure import StructDCTStandard
from pkan.dcatapde.structure.structure import StructFOAFAgent
from pkan.dcatapde.structure.structure import StructSKOSConcept
from pkan.dcatapde.structure.structure import StructSKOSConceptScheme
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

    def test_dcat_catalog_struct(self):
        base = StructDCATCatalog()
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dcat_dataset_struct(self):
        base = StructDCATDataset()
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dcat_distribution_struct(self):
        base = StructDCATDistribution()
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dct_licensedocument_struct(self):
        base = StructDCTLicenseDocument()
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dct_location_struct(self):
        base = StructDCTLocation()
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dct_mediatypeorextent(self):
        base = StructDCTMediaTypeOrExtent()
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dct_standard_struct(self):
        base = StructDCTStandard()
        self.assertGreater(len(base.vocab_terms), 0)

    def test_foaf_agent_struct(self):
        base = StructFOAFAgent()
        self.assertGreater(len(base.vocab_terms), 0)

    def test_skos_concept_struct(self):
        base = StructSKOSConcept()
        self.assertGreater(len(base.vocab_terms), 0)

    def test_skos_conceptscheme_struct(self):
        base = StructSKOSConceptScheme()
        self.assertGreater(len(base.vocab_terms), 0)
