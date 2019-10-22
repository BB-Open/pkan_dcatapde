# -*- coding: utf-8 -*-
"""Test license document related vocabularies."""
from pkan.dcatapde import constants
from pkan.dcatapde import testing
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized

import unittest


class BaseTestMixin():

    def vocab_test(self, vocab_name):
        api.content.transition(obj=self.item1, transition='activate')
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(len(vocabulary), 1)
        self.assertEqual(
            vocabulary.getTerm(self.item1.UID()).title,
            self.item1.Title(),
        )

    def vocab_test_formatted(self, vocab_name):
        api.content.transition(obj=self.item1, transition='activate')
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(len(vocabulary), 1)
        self.assertEqual(
            vocabulary.getTerm(self.item1.UID()).title,
            '{0} ({1})'.format(
                self.item1.Title(),
                self.item1.rdfs_isDefinedBy,
            ),
        )


class TestDCATCatalogVocabulary(unittest.TestCase, BaseTestMixin):
    """Validate the `DCATCatalogVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_CATALOG,
            id='catalog-1',
            dct_title={'deu': u'Catalog 1'},
        )

        self.item2 = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_CATALOG,
            id='catalog-2',
            dct_title={'deu': u'Catalog 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.DCATCatalog'
        self.vocab_test(vocab_name)


class TestDCATDatasetVocabulary(unittest.TestCase, BaseTestMixin):
    """Validate the `DCATDatasetVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.catalog = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_CATALOG,
            id='catalog-1',
            dct_title={'deu': u'Catalog 1'},
        )
        self.item1 = api.content.create(
            container=self.catalog,
            type=constants.CT_DCAT_DATASET,
            id='dataset-1',
            dct_title={'deu': u'Dataset 1'},
        )
        self.item2 = api.content.create(
            container=self.catalog,
            type=constants.CT_DCAT_DATASET,
            id='dataset-2',
            dct_title={'deu': u'Dataset 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.DCATDataset'
        self.vocab_test(vocab_name)


class TestDCATDistributionVocabulary(unittest.TestCase, BaseTestMixin):
    """Validate the `DCATDistributionVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.cat = api.content.create(
            container=self.portal,
            type=constants.CT_DCAT_CATALOG,
            id='catalog-1',
            dct_title={'deu': u'Catalog 1'},
        )
        self.dataset = api.content.create(
            container=self.cat,
            type=constants.CT_DCAT_DATASET,
            id=constants.CT_DCAT_DATASET,
        )
        self.item1 = api.content.create(
            container=self.dataset,
            type=constants.CT_DCAT_DISTRIBUTION,
            id='distribution-1',
            dct_title={'deu': u'Distribution 1'},
        )
        self.item2 = api.content.create(
            container=self.dataset,
            type=constants.CT_DCAT_DISTRIBUTION,
            id='distribution-2',
            dct_title={'deu': u'Distribution 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.DCATDistribution'
        self.vocab_test(vocab_name)


class TestDCTLicenseDocumentVocabulary(unittest.TestCase, BaseTestMixin):
    """Validate the `DCTLicenseDocumentVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal.get(constants.FOLDER_LICENSES),
            type=constants.CT_DCT_LICENSEDOCUMENT,
            id='license-1',
            dct_title={'deu': u'License 1'},
            rdfs_isDefinedBy='https://example.com/license-1',
        )
        self.item2 = api.content.create(
            container=self.portal.get(constants.FOLDER_LICENSES),
            type=constants.CT_DCT_LICENSEDOCUMENT,
            id='license-2',
            dct_title={'deu': u'License 2'},
            rdfs_isDefinedBy='https://example.com/license-2',
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.DCTLicenseDocument'
        self.vocab_test_formatted(vocab_name)


class TestDCTLocationVocabulary(unittest.TestCase, BaseTestMixin):
    """Validate the `DCTLocationVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal.get(constants.FOLDER_LOCATIONS),
            type=constants.CT_DCT_LOCATION,
            id='location-1',
            dct_title={'deu': u'Location 1'},
            rdfs_isDefinedBy='https://example.com/location-1',
        )
        self.item2 = api.content.create(
            container=self.portal.get(constants.FOLDER_LOCATIONS),
            type=constants.CT_DCT_LOCATION,
            id='location-2',
            dct_title={'deu': u'Location 2'},
            rdfs_isDefinedBy='https://example.com/location-2',
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.DCTLocation'
        self.vocab_test_formatted(vocab_name)


class TestDCTMediaTypeOrExtentVocabulary(unittest.TestCase, BaseTestMixin):
    """Validate the `DCTMediaTypeOrExtentVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal.get(constants.FOLDER_MEDIATYPES),
            type=constants.CT_DCT_MEDIATYPEOREXTENT,
            id='mediatype-1',
            dct_title={'deu': 'Mediatype 1'},
        )
        self.item2 = api.content.create(
            container=self.portal.get(constants.FOLDER_MEDIATYPES),
            type=constants.CT_DCT_MEDIATYPEOREXTENT,
            id='mediatype-2',
            dct_title={'deu': u'Mediatype 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.DCTMediaTypeOrExtent'
        self.vocab_test(vocab_name)


class TestDCTStandardVocabulary(unittest.TestCase, BaseTestMixin):
    """Validate the `DCTStandardVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal.get(constants.FOLDER_STANDARDS),
            type=constants.CT_DCT_STANDARD,
            id='standard-1',
            dct_title={'deu': u'Standard 1'},
        )
        self.item2 = api.content.create(
            container=self.portal.get(constants.FOLDER_STANDARDS),
            type=constants.CT_DCT_STANDARD,
            id='standard-2',
            dct_title={'deu': u'Standard 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.DCTStandard'
        self.vocab_test_formatted(vocab_name)


class TestFOAFAgentVocabulary(unittest.TestCase, BaseTestMixin):
    """Validate the `FOAFAgentVocabulary` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal.get(constants.FOLDER_AGENTS),
            type=constants.CT_FOAF_AGENT,
            id='agent-1',
            foaf_name={'deu': u'Agent 1'},
        )
        self.item2 = api.content.create(
            container=self.portal.get(constants.FOLDER_AGENTS),
            type=constants.CT_FOAF_AGENT,
            id='agent-2',
            foaf_name={'deu': u'Agent 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.FOAFAgent'
        self.vocab_test(vocab_name)


class TestSKOSConceptVocabulary(unittest.TestCase, BaseTestMixin):
    """Validate the `SKOSConcept` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal.get(constants.FOLDER_CONCEPTS),
            type=constants.CT_SKOS_CONCEPT,
            id='concept-1',
            dct_title={'deu': u'Concept 1'},
        )
        self.item2 = api.content.create(
            container=self.portal.get(constants.FOLDER_CONCEPTS),
            type=constants.CT_SKOS_CONCEPT,
            id='concept-2',
            dct_title={'deu': u'Concept 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.SKOSConcept'
        self.vocab_test(vocab_name)


class TestSKOSConceptSchemeVocabulary(unittest.TestCase, BaseTestMixin):
    """Validate the `SKOSConceptScheme` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal.get(constants.FOLDER_CONCEPTSCHEMES),
            type=constants.CT_SKOS_CONCEPTSCHEME,
            id='concept-1',
            dct_title={'deu': u'Concept Scheme 1'},
        )
        self.item2 = api.content.create(
            container=self.portal.get(constants.FOLDER_CONCEPTSCHEMES),
            type=constants.CT_SKOS_CONCEPTSCHEME,
            id='concept-2',
            dct_title={'deu': u'Concept Scheme 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.SKOSConceptScheme'
        self.vocab_test(vocab_name)


class TestDcatTypesVocabulary(unittest.TestCase, BaseTestMixin):
    """Validate the `SKOSConceptScheme` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal.get(constants.FOLDER_CONCEPTSCHEMES),
            type=constants.CT_SKOS_CONCEPTSCHEME,
            id='concept-2',
            dct_title={'deu': 'Concept Scheme 1'},
        )
        self.item2 = api.content.create(
            container=self.portal.get(constants.FOLDER_CONCEPTSCHEMES),
            type=constants.CT_SKOS_CONCEPTSCHEME,
            id='concept-3',
            dct_title={'deu': 'Concept Scheme 2'},
        )
        self.item3 = api.content.create(
            container=self.portal.get(constants.FOLDER_AGENTS),
            type=constants.CT_FOAF_AGENT,
            id='agent-3',
            foaf_name={'deu': u'Agent 1'},
        )
        self.item4 = api.content.create(
            container=self.portal.get(constants.FOLDER_AGENTS),
            type=constants.CT_FOAF_AGENT,
            id='agent-4',
            foaf_name={'deu': u'Agent 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.AllDcatObjects'
        api.content.transition(obj=self.item1, transition='activate')
        api.content.transition(obj=self.item3, transition='activate')
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))

        self.assertEqual(len(vocabulary), 2)
        self.assertEqual(
            vocabulary.getTerm(self.item1.UID()).title,
            self.item1.Title(),
        )
        self.assertEqual(
            vocabulary.getTerm(self.item3.UID()).title,
            self.item3.Title(),
        )


class TestVCARDKindVocabulary(unittest.TestCase, BaseTestMixin):
    """Validate the `SKOSConceptScheme` vocabulary."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.item1 = api.content.create(
            container=self.portal.get(constants.FOLDER_VCARD_KIND),
            type=constants.CT_VCARD_KIND,
            id='contact-1',
            dct_title={'deu': u'Concept Scheme 1'},
        )
        self.item2 = api.content.create(
            container=self.portal.get(constants.FOLDER_VCARD_KIND),
            type=constants.CT_VCARD_KIND,
            id='contact-2',
            dct_title={'deu': u'Concept Scheme 2'},
        )

    def test_vocabulary(self):
        """Validate the vocabulary."""
        vocab_name = 'pkan.dcatapde.vocabularies.VCARDKind'
        self.vocab_test(vocab_name)
