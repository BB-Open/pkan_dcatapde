# -*- coding: utf-8 -*-
"""Vocabularies and sources for content types."""

from pkan.dcatapde import constants
from pkan.dcatapde.vocabularies import utils
from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class BaseContentTypeVocabulary(object):
    """A vocabulary returning a list of objects from a content type."""

    portal_type = None

    def get_results(self, query):
        params = {
            'portal_type': self.portal_type,
        }
        query.update(params)

        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog(query)
        terms = []

        for brain in brains:
            obj = brain.getObject()
            terms.append(
                SimpleTerm(
                    value=brain.UID,
                    token=str(brain.UID),
                    title=obj.title_for_vocabulary(),
                ),
            )

        return SimpleVocabulary(terms)

    def __call__(self, context, query=None):
        query = utils.parse_query(context=context, query=query)
        return self.get_results(query=query)


@implementer(IVocabularyFactory)
class DCATCatalogVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning DCATCatalog items."""

    portal_type = constants.CT_DCAT_CATALOG


DCATCatalogVocabularyFactory = DCATCatalogVocabulary()


@implementer(IVocabularyFactory)
class DCATDatasetVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning DCATDataset items."""

    portal_type = constants.CT_DCAT_DATASET


DCATDatasetVocabularyFactory = DCATDatasetVocabulary()


@implementer(IVocabularyFactory)
class DCATDistributionVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning DCATDistribution items."""

    portal_type = constants.CT_DCAT_DISTRIBUTION


DCATDistributionVocabularyFactory = DCATDistributionVocabulary()


@implementer(IVocabularyFactory)
class DCTLicenseDocumentVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning DCTLicenseDocument items."""

    portal_type = constants.CT_DCT_LICENSEDOCUMENT


DCTLicenseDocumentVocabularyFactory = DCTLicenseDocumentVocabulary()


@implementer(IVocabularyFactory)
class DCTLocationVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning DCTLocation items."""

    portal_type = constants.CT_DCT_LOCATION


DCTLocationVocabularyFactory = DCTLocationVocabulary()


@implementer(IVocabularyFactory)
class DCTMediaTypeOrExtentVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning DCTMediaTypeOrExtent items."""

    portal_type = constants.CT_DCT_MEDIATYPEOREXTENT


DCTMediaTypeOrExtentVocabularyFactory = DCTMediaTypeOrExtentVocabulary()


@implementer(IVocabularyFactory)
class DCTStandardVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning DCTStandard items."""

    portal_type = constants.CT_DCT_STANDARD


DCTStandardVocabularyFactory = DCTStandardVocabulary()


@implementer(IVocabularyFactory)
class DCTRightsStatementVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning DCTRightsStatement items."""

    portal_type = constants.CT_DCT_RIGHTSSTATEMENT


DCTRightsStatementVocabularyFactory = DCTRightsStatementVocabulary()


@implementer(IVocabularyFactory)
class FOAFAgentVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning FOAFAgent items."""

    portal_type = constants.CT_FOAF_AGENT


FOAFAgentVocabularyFactory = FOAFAgentVocabulary()


@implementer(IVocabularyFactory)
class SKOSConceptVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning SKOSConcept items."""

    portal_type = constants.CT_SKOS_CONCEPT


SKOSConceptVocabularyFactory = SKOSConceptVocabulary()


@implementer(IVocabularyFactory)
class SKOSConceptSchemeVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning SKOSConceptScheme items."""

    portal_type = constants.CT_SKOS_CONCEPTSCHEME


SKOSConceptSchemeVocabularyFactory = SKOSConceptSchemeVocabulary()


@implementer(IVocabularyFactory)
class AllDcatObjectsVocabulary(BaseContentTypeVocabulary):

    portal_type = constants.DCAT_CTs


AllDcatObjectsVocabularyFactory = AllDcatObjectsVocabulary()
