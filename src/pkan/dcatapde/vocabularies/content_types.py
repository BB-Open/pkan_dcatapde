# -*- coding: utf-8 -*-
"""Vocabularies and sources for content types."""
from BTrees._IIBTree import intersection
from pkan.dcatapde import constants
from pkan.dcatapde.api.functions import query_active_objects
from pkan.dcatapde.api.functions import query_objects_no_pkanstate
from pkan.dcatapde.browser.add_views.default_add_view import PkanDefaultAddForm
from pkan.dcatapde.constants import CT_CONCEPT_FOLDER
from pkan.dcatapde.constants import DCAT_CTs
from pkan.dcatapde.constants import FOLDER_CONCEPTS
from pkan.dcatapde.i18n import CT_LABELS
from pkan.dcatapde.utils import get_request_annotations
from pkan.dcatapde.vocabularies import utils as vutils
from plone import api
from plone.app.vocabularies.catalog import KeywordsVocabulary
from plone.app.vocabularies.terms import safe_encode
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IContextSourceBinder)
class BaseContentTypeVocabulary(object):
    """A vocabulary returning a list of objects from a content type."""

    portal_type = None

    def get_results(self, query, context):
        # todo: isinstance is not nice, but if its another form,
        # it does not set this annotations
        if isinstance(context, PkanDefaultAddForm):
            context = get_request_annotations('pkan.vocabularies.context')

        brains = query_active_objects(query, self.portal_type, context=context)

        uids = []
        terms = []

        for brain in brains:
            obj = brain.getObject()
            if brain.UID in uids:
                # todo: how can this happen?
                continue
            uids.append(brain.UID)
            terms.append(
                SimpleTerm(
                    value=brain.UID,
                    token=str(brain.UID),
                    title=obj.title_for_vocabulary(),
                ),
            )

        return SimpleVocabulary(terms)

    def __call__(self, context, query=None):
        query = vutils.parse_query(context=context, query=query)
        return self.get_results(query=query, context=context)


@provider(IContextSourceBinder)
class BaseContentTypeVocabularyNoPkanState(BaseContentTypeVocabulary):

    def get_results(self, query, context):
        if isinstance(context, PkanDefaultAddForm):
            context = get_request_annotations('pkan.vocabularies.context')
        brains = query_objects_no_pkanstate(query,
                                            self.portal_type,
                                            context=context)

        uids = []
        terms = []

        for brain in brains:
            obj = brain.getObject()
            if brain.UID in uids:
                # todo: how can this happen?
                continue
            uids.append(brain.UID)
            terms.append(
                SimpleTerm(
                    value=brain.UID,
                    token=str(brain.UID),
                    title=obj.title_for_vocabulary(),
                ),
            )

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class DCATCatalogVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning DCATCatalog items."""

    portal_type = constants.CT_DCAT_CATALOG


DCATCatalogVocabularyFactory = DCATCatalogVocabulary()


@implementer(IVocabularyFactory)
class DcatCatalogContextAwareVocabulary(BaseContentTypeVocabularyNoPkanState):
    """A vocabulary returning all objects from portal catalog."""

    portal_type = constants.CT_DCAT_CATALOG

    def __call__(self, context, query=None):
        query = vutils.parse_query(context=context, query=query)
        if context:
            query['path'] = '/'.join(context.getPhysicalPath())
        return self.get_results(query, context)

ContextAwareCatalogFactory = DcatCatalogContextAwareVocabulary()


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
class HarvesterVocabulary(BaseContentTypeVocabularyNoPkanState):
    """A vocabulary returning Harvester items."""

    portal_type = constants.CT_HARVESTER


HarvesterVocabularyFactory = HarvesterVocabulary()


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
class VCARDKindVocabulary(BaseContentTypeVocabulary):
    """A vocabulary returning SKOSConceptScheme items."""

    portal_type = constants.CT_VCARD_KIND


VCARDKindVocabularyFactory = VCARDKindVocabulary()


@implementer(IVocabularyFactory)
class AllDcatObjectsVocabulary(BaseContentTypeVocabulary):

    portal_type = constants.DCAT_CTs


AllDcatObjectsVocabularyFactory = AllDcatObjectsVocabulary()


@implementer(IVocabularyFactory)
class AllDCATPortalTypesVocabulary(object):

    def __call__(self, *args, **kwargs):
        terms = []
        for ct in DCAT_CTs:
            ct_label = CT_LABELS[ct]
            terms.append(SimpleTerm(ct, ct, ct_label))

        return SimpleVocabulary(terms)

AllDCATPortalTypesVocabularyFactory = AllDCATPortalTypesVocabulary()


@implementer(IVocabularyFactory)
class SKOSConceptValueVocabulary(KeywordsVocabulary):

    keyword_index = 'dcat_theme'

    def safe_simplevocabulary_from_values(self, values, query=None):
        """Creates (filtered) SimpleVocabulary from iterable of untrusted values.
        """
        terms = []
        for i in values:
            if query is None or safe_encode(query) in safe_encode(i):
                obj = api.content.get(UID=i)
                if not obj:
                    continue
                title = str(obj.dct_title)
                term = SimpleTerm(i, i, title)
                terms.append(term)
        return SimpleVocabulary(terms)

    def all_keywords(self, kwfilter):
        self.catalog = api.portal.get_tool('portal_catalog')
        if self.catalog is None:
            return SimpleVocabulary([])
        index = self.catalog._catalog.getIndex(self.keyword_index)
        voc = self.safe_simplevocabulary_from_values(
            index._index,
            query=kwfilter,
        )
        return voc

    def keywords_of_section(self, section, kwfilter):
        """Valid keywords under the given section.
        """
        pcat = api.portal.get_tool('portal_catalog')
        cat = pcat._catalog
        path_idx = cat.indexes[self.path_index]
        tags_idx = cat.indexes[self.keyword_index]
        result = []
        # query all oids of path - low level
        pquery = {
            self.path_index: {
                'query': '/'.join(section.getPhysicalPath()),
                'depth': -1,
            },
        }
        kwfilter = safe_encode(kwfilter)
        # uses internal zcatalog specific details to quickly get the values.
        path_result, info = path_idx._apply_index(pquery)
        for tag in tags_idx.uniqueValues():
            if kwfilter and kwfilter not in safe_encode(tag):
                continue
            tquery = {self.keyword_index: tag}
            tags_result, info = tags_idx._apply_index(tquery)
            if intersection(path_result, tags_result):
                result.append(tag)
        # result should be sorted, because uniqueValues are.
        return self.safe_simplevocabulary_from_values(result)

    def __call__(self, context, query=None):
        section = self.section(context)
        if section is None:
            return self.all_keywords(query)
        return self.keywords_of_section(section, query)

SKOSConceptValueVocabularyFactory = SKOSConceptValueVocabulary()


@implementer(IVocabularyFactory)
class SKOSConceptDefaultVocabulary(KeywordsVocabulary):

    def safe_simplevocabulary_from_values(self, values):
        """Creates (filtered) SimpleVocabulary from iterable of untrusted values.
        """
        terms = []
        for id, obj in values:
            title = obj.Title()
            uid = obj.UID()
            term = SimpleTerm(uid, uid, title)
            terms.append(term)
        return SimpleVocabulary(terms)

    def all_keywords(self):
        self.catalog = api.portal.get_tool('portal_catalog')
        if self.catalog is None:
            return SimpleVocabulary([])
        parent_brain = api.content.find(
            portal_type=CT_CONCEPT_FOLDER,
            title=FOLDER_CONCEPTS,
        )
        parent = parent_brain[0].getObject()
        voc = self.safe_simplevocabulary_from_values(
            parent.contentItems(),
        )
        return voc

    def __call__(self, context, query=None):
        return self.all_keywords()

SKOSConceptDefaultVocabularyFactory = SKOSConceptDefaultVocabulary()
