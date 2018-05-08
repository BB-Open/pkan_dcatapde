# -*- coding: utf-8 -*-
"""tests for `structure`."""

from pkan.dcatapde import testing
from pkan.dcatapde.structure.structure import StructBase
from pkan.dcatapde.structure.structure import StructDCATCatalog
from pkan.dcatapde.structure.structure import StructDCATDataset
from pkan.dcatapde.structure.structure import StructDCATDistribution
from pkan.dcatapde.structure.structure import StructDCTLanguage
from pkan.dcatapde.structure.structure import StructDCTLicenseDocument
from pkan.dcatapde.structure.structure import StructDCTLocation
from pkan.dcatapde.structure.structure import StructDCTMediaTypeOrExtent
from pkan.dcatapde.structure.structure import StructDCTStandard
from pkan.dcatapde.structure.structure import StructFOAFAgent
from pkan.dcatapde.structure.structure import StructSKOSConcept
from pkan.dcatapde.structure.structure import StructSKOSConceptScheme
from pkan.dcatapde.structure.structure import StructVCARDKind
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class StructureTest(unittest.TestCase):
    """Validate the `structure classes`."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_base_struct(self):
        base = StructBase('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dcat_catalog_struct(self):
        base = StructDCATCatalog('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dcat_dataset_struct(self):
        base = StructDCATDataset('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dcat_distribution_struct(self):
        base = StructDCATDistribution('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dct_licensedocument_struct(self):
        base = StructDCTLicenseDocument('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dct_location_struct(self):
        base = StructDCTLocation('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dct_language_struct(self):
        base = StructDCTLanguage('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dct_mediatypeorextent(self):
        base = StructDCTMediaTypeOrExtent('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)

    def test_dct_standard_struct(self):
        base = StructDCTStandard('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)

    def test_foaf_agent_struct(self):
        base = StructFOAFAgent('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)

    def test_skos_concept_struct(self):
        base = StructSKOSConcept('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)

    def test_skos_conceptscheme_struct(self):
        base = StructSKOSConceptScheme('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)

    def test_vcard_kind_struct(self):
        base = StructVCARDKind('dummy context')
        self.assertGreater(len(base.vocab_terms), 0)
