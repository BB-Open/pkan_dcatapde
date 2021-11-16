# -*- coding: utf-8 -*-
"""Structure of the dcat-AP.de scheme"""
from datetime import datetime
from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import CT_DCAT_COLLECTION_CATALOG
from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.constants import CT_DCAT_DISTRIBUTION
from pkan.dcatapde.constants import CT_DCT_LANGUAGE
from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.constants import CT_DCT_LOCATION
from pkan.dcatapde.constants import CT_DCT_MEDIATYPEOREXTENT
from pkan.dcatapde.constants import CT_DCT_RIGHTSSTATEMENT
from pkan.dcatapde.constants import CT_DCT_STANDARD
from pkan.dcatapde.constants import CT_FOAF_AGENT
from pkan.dcatapde.constants import CT_RDFS_LITERAL
from pkan.dcatapde.constants import CT_SKOS_CONCEPT
from pkan.dcatapde.constants import CT_SKOS_CONCEPTSCHEME
from pkan.dcatapde.constants import CT_VCARD_KIND
from pkan.dcatapde.constants import FIELD_BLACKLIST
from pkan.dcatapde.content.dcat_catalog import IDCATCatalog
from pkan.dcatapde.content.dcat_collectioncatalog import IDCATCollectionCatalog
from pkan.dcatapde.content.dcat_dataset import IDCATDataset
from pkan.dcatapde.content.dcat_distribution import IDCATDistribution
from pkan.dcatapde.content.dct_language import IDCTLanguage
from pkan.dcatapde.content.dct_licensedocument import IDCTLicenseDocument
from pkan.dcatapde.content.dct_location import IDCTLocation
from pkan.dcatapde.content.dct_mediatypeorextent import IDCTMediaTypeOrExtent
from pkan.dcatapde.content.dct_rightsstatement import IDCTRightsStatement
from pkan.dcatapde.content.dct_standard import IDCTStandard
from pkan.dcatapde.content.foaf_agent import IFOAFAgent
from pkan.dcatapde.content.rdfs_literal import IRDFSLiteral
from pkan.dcatapde.content.skos_concept import ISKOSConcept
from pkan.dcatapde.content.skos_conceptscheme import ISKOSConceptScheme
from pkan.dcatapde.content.vcard_kind import IVCARDKind
from pkan.dcatapde.structure.interfaces import IStructure
from pkan.dcatapde.structure.namespaces import DCAT
from pkan.dcatapde.structure.namespaces import DCT
from pkan.dcatapde.structure.namespaces import INIT_NS
from pkan.dcatapde.structure.namespaces import VCARD
from pkan.dcatapde.utils import get_current_language
from plone.api import portal
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
# todo: do we want to import plone for Namedfiles
from plone.namedfile.file import NamedFile
from plone.supermodel.interfaces import FIELDSETS_KEY
from rdflib.namespace import FOAF
from rdflib.namespace import RDFS
from rdflib.namespace import SKOS
from zope.component import adapter
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.schema import getFieldsInOrder
from zope.schema.vocabulary import SimpleTerm

import rdflib

IMP_OPTIONAL = 'optional'
IMP_RECOMENDED = 'recommended'
IMP_REQUIRED = 'required'


def non_fieldset_fields(schema):
    """Return fields not in fieldset."""
    fieldset_fields = []
    fieldsets = schema.queryTaggedValue(FIELDSETS_KEY, [])

    for fieldset in fieldsets:
        fieldset_fields.extend(fieldset.fields)

    fields = [info[0] for info in getFieldsInOrder(schema)]

    return [f for f in fields if f not in fieldset_fields]


def get_ordered_fields(fti):
    """Return fields in fieldset order.

    NOTE: code extracted from collective.excelexport. Original comments
    preserved

    this code is much complicated because we have to get sure
    we get the fields in the order of the fieldsets
    the order of the fields in the fieldsets can differ
    of the getFieldsInOrder(schema) order...
    that's because fields from different schemas
    can take place in the same fieldset
    """
    schema = fti.lookupSchema()
    fieldset_fields = {}
    ordered_fieldsets = ['default']

    for fieldset in schema.queryTaggedValue(FIELDSETS_KEY, []):
        ordered_fieldsets.append(fieldset.__name__)
        fieldset_fields[fieldset.__name__] = fieldset.fields

    if fieldset_fields.get('default', []):
        fieldset_fields['default'] += non_fieldset_fields(schema)
    else:
        fieldset_fields['default'] = non_fieldset_fields(schema)

    # Get the behavior fields
    fields = getFieldsInOrder(schema)

    for behavior_id in fti.behaviors:
        schema = getUtility(IBehavior, behavior_id).interface

        if not IFormFieldProvider.providedBy(schema):
            continue

        fields.extend(getFieldsInOrder(schema))

        for fieldset in schema.queryTaggedValue(FIELDSETS_KEY, []):
            fieldset_fields.setdefault(
                fieldset.__name__, []).extend(fieldset.fields)
            ordered_fieldsets.append(fieldset.__name__)

        fieldset_fields['default'].extend(non_fieldset_fields(schema))

    ordered_fields = []

    for fieldset in ordered_fieldsets:
        ordered_fields.extend(fieldset_fields[fieldset])

    fields.sort(key=lambda field: ordered_fields.index(field[0]))

    return fields


@implementer(IStructure)
@adapter(IDexterityFTI)
class StructBase(object):
    """Utility functions for all structure classes"""

    # The content type this structure represents
    portal_type = None
    # List of fields that can act as title for dx object creation
    title_field = ['dct_title']
    desc_field = ['dct_description']

    literal_field = None

    # caching
    _fields_in_order = None
    _fields_objects_required = {}
    # List of DX fields to ignore at output
    _blacklist = FIELD_BLACKLIST
    # List of fields which shounld not be required
    _not_required = []

    # the list dict of properties formerly from Plone
    # now to be implemented explizit
    _properties = {}

    def __init__(self, context):
        self.context = context

    @property
    def fields_in_order(self):
        if not self._fields_in_order:
            ptypes = portal.get_tool('portal_types')
            if self.portal_type in ptypes:
                fti = ptypes[self.portal_type]
                self._fields_in_order = get_ordered_fields(fti)
            else:
                self._fields_in_order = []
        return self._fields_in_order

    @property
    def properties(self):
        """Return properties.

        :return:
        """

        result = {}
        if self._properties is not None:
            return self._properties

        for field_name, field in self.fields_in_order:
            if field_name in self._blacklist:
                continue

            if field.required and field_name not in self._not_required:
                importance = IMP_REQUIRED
            else:
                importance = IMP_OPTIONAL

            result[field_name] = {
                'object': StructRDFSLiteral,
                'importance': importance,
                'predicate': self.fieldname2predicate(field_name),
                'type': field._type,
            }

        # add subjects
        result['subject'] = {
            'object': StructRDFSLiteral,
            'importance': IMP_OPTIONAL,
            'predicate': DCAT.keyword,
            'type': list,
            'rdf_name': 'dcat_keyword',
        }
        result['subjects'] = {
            'object': StructRDFSLiteral,
            'importance': IMP_OPTIONAL,
            'predicate': DCAT.keyword,
            'type': list,
            'rdf_name': 'dcat_keyword',
        }

        return result

    @property
    def contained(self):
        """Return all predicates that are modelled as contained instances.

        :return:
        """
        result = {}
        return result

    @property
    def referenced(self):
        """Return all predicates that are modelle as references instances

        :return:
        """
        related = {}
        return related

    def fieldname2predicate(self, fieldname):
        """Derives a namespace based predicate out of a fieldname"""
        # split fieldname at the first underscore
        fieldname_split = fieldname.split('_')
        ns = fieldname_split[0]
        cls = '_'.join(fieldname_split[1:])
        # try to identify a namespace
        if ns in INIT_NS:
            NS = INIT_NS[ns]
            # get the namespace binding
            predicate = getattr(NS, cls)
        else:
            predicate = fieldname
        return predicate

    @property
    def fields_and_referenced(self):
        """Return all predicates, their objects types and if they are
        required"""

        if not self._fields_objects_required:
            self._fields_objects_required = {}
            # First the properties
            # Then the contained
            for field_name in self.properties:
                property = self.properties[field_name]
                self._fields_objects_required[field_name] = property

            # Then the referenced
            for field_name in self.referenced:
                referenced = self.referenced[field_name]
                self._fields_objects_required[field_name] = referenced

        return self._fields_objects_required

    def field2token(self, field_name, field, importance=None):
        """Calculate a token for the vocab terms and the parser"""
        if not importance:
            importance = field['importance']
        if importance == IMP_REQUIRED:
            token = '{CT}__{field_name}__required'.format(
                CT=self.portal_type,
                field_name=field_name,
            )
        else:
            token = '{CT}__{field_name}'.format(
                CT=self.portal_type,
                field_name=field_name,
            )
        return token

    @property
    def vocab_terms(self):
        """Terms for a vocabulary. The tokens hold the subjects CT,
        and the predicate. The objects type information is neglected."""

        field_names = sorted(self.fields_and_referenced.keys())

        terms = []
        for field_name in field_names:
            importance = self.fields_and_referenced[field_name]['importance']
            if importance == IMP_REQUIRED:
                title = _(
                    u'${CT}=>${field_name} (required)',
                    mapping={
                        u'field_name': u'{0}'.format(field_name),
                        u'CT': u'{0}'.format(self.portal_type),
                    },
                )
            else:
                title = _(
                    u'${CT}=>${field_name}',
                    mapping={
                        u'field_name': u'{0}'.format(field_name),
                        u'CT': u'{0}'.format(self.portal_type),
                    },
                )

            token = self.field2token(
                field_name,
                self.fields_and_referenced[field_name],
            )

            title = translate(
                title,
                target_language=get_current_language(),
            )
            terms.append(
                SimpleTerm(
                    value=token, token=token, title=title,
                ),
            )
        return terms


# todo, check if properties schould be referenced


@implementer(IStructure)
@adapter(IDCATCatalog)
class StructDCATCatalog(StructBase):
    """Structure definition of dcat:Catalog"""

    portal_type = CT_DCAT_CATALOG
    rdf_type = DCAT.Catalog
    predicate = 'dcat:catalog'

    @property
    def properties(self):
        return {
            'dct_identifier': {'object': StructRDFSLiteral,
                               'importance': 'optional',
                               'predicate': rdflib.term.URIRef(
                                   'http://purl.org/dc/terms/identifier'),
                               'type': str},
            'adms_identifier': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://www.w3.org/ns/adms#identifier'),
                                'type': str},
            'dct_title': {'object': StructRDFSLiteral,
                          'importance': 'required',
                          'predicate': rdflib.term.URIRef(
                              'http://purl.org/dc/terms/title'),
                          'type': dict},
            'dct_description': {'object': StructRDFSLiteral,
                                'importance': 'required',
                                'predicate': rdflib.term.URIRef(
                                    'http://purl.org/dc/terms/description'),
                                'type': dict},
            'foaf_homepage': {'object': StructRDFSLiteral,
                              'importance': 'optional',
                              'predicate': rdflib.term.URIRef(
                                  'http://xmlns.com/foaf/0.1/homepage'),
                              'type': str},
            'dct_language': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://purl.org/dc/terms/language'),
                             'type': list},
            'dcat_themeTaxonomy': {'object': StructRDFSLiteral,
                                   'importance': 'optional',
                                   'predicate': rdflib.term.URIRef(
                                       'http://www.w3.org/ns/dcat#themeTaxonomy',  # noqa: E501
                                   ),
                                   'type': None},
            'dct_issued': {'object': StructRDFSLiteral,
                           'importance': 'optional',
                           'predicate': rdflib.term.URIRef(
                               'http://purl.org/dc/terms/issued'),
                           'type': datetime.date},
            'dct_modified': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://purl.org/dc/terms/modified'),
                             'type': datetime.date},
            'dct_hasPart': {'object': StructRDFSLiteral,
                            'importance': 'optional',
                            'predicate': rdflib.term.URIRef(
                                'http://purl.org/dc/terms/hasPart'),
                            'type': None},
            'dct_isPartOf': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://purl.org/dc/terms/isPartOf'),
                             'type': None},
            'subjects': {'object': StructRDFSLiteral,
                         'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://www.w3.org/ns/dcat#keyword'),
                         'type': list},
            'language': {'object': StructRDFSLiteral,
                         'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://purl.org/dc/terms/language'),
                         'type': None}, 'subject': {
                'object': StructRDFSLiteral,
                'importance': 'optional',
                'predicate': rdflib.term.URIRef(
                    'http://www.w3.org/ns/dcat#keyword'),
                'type': list,
                'rdf_name': 'dcat_keyword'}}

    @property
    def contained(self):
        """Return all contained items.

        :return:
        """
        result = {}
        result['dcat_dataset'] = {
            'object': StructDCATDataset,
            'importance': IMP_REQUIRED,
            'type': list,
            'predicate': DCAT.dataset,
            'target': DCAT.Dataset,
        }
        return result

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        related = {}
        related['dct_publisher'] = {
            'object': StructFOAFAgent,
            'importance': IMP_REQUIRED,
            # 'importance': IMP_OPTIONAL,
            'type': str,
            'predicate': DCT.publisher,
            'target': FOAF.Agent,
        }
        related['dct_license'] = {
            'object': StructDCTLicenseDocument,
            'importance': IMP_OPTIONAL,
            'type': str,
            'predicate': DCT.license,
            'target': DCT.LicenseDocument,
        }
        related['dct_rights'] = {
            'object': StructDCTRightsStatement,
            'importance': IMP_OPTIONAL,
            'type': str,
            'predicate': DCT.rights,
            'target': DCT.RightsStatement,
        }
        related['dct_spatial'] = {
            'object': StructDCTLocation,
            'importance': IMP_OPTIONAL,
            'type': list,
            'predicate': DCT.spatial,
            'target': DCT.Location,
        }
        return related


@implementer(IStructure)
@adapter(IDCATCollectionCatalog)
class StructDCATCollectionCatalog(StructDCATCatalog):
    """
    Structure definition for CollectionCatalog
    """

    portal_type = CT_DCAT_COLLECTION_CATALOG
    rdf_type = DCAT.Catalog
    predicate = DCAT.catalog

    @property
    def contained(self):
        """Return all contained items.

        :return:
        """
        result = {}
        result['dcat_catalog'] = {
            'object': StructDCATCatalog,
            'importance': IMP_REQUIRED,
            'type': list,
            'predicate': DCAT.catalog,
            'target': DCAT.Catalog,
        }
        return result


@implementer(IStructure)
@adapter(IDCATDataset)
class StructDCATDataset(StructBase):
    portal_type = CT_DCAT_DATASET
    rdf_type = DCAT.Dataset

    @property
    def properties(self):
        return {'dct_identifier': {'object': StructRDFSLiteral,
                                   'importance': 'optional',
                                   'predicate': rdflib.term.URIRef(
                                       'http://purl.org/dc/terms/identifier'),
                                   'type': str},
                'adms_identifier': {'object': StructRDFSLiteral,
                                    'importance': 'optional',
                                    'predicate': rdflib.term.URIRef(
                                        'http://www.w3.org/ns/adms#identifier'),  # noqa: E501
                                    'type': str},
                'dct_title': {'object': StructRDFSLiteral,
                              'importance': 'required',
                              'predicate': rdflib.term.URIRef(
                                  'http://purl.org/dc/terms/title'),
                              'type': dict},
                'dct_creator': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://purl.org/dc/terms/creator'),
                                'type': None},
                'dct_contributor': {'object': StructRDFSLiteral,
                                    'importance': 'optional',
                                    'predicate': rdflib.term.URIRef(
                                        'http://purl.org/dc/terms/contributor'),  # noqa: E501
                                    'type': None},
                'dcatde_originator': {'object': StructRDFSLiteral,
                                      'importance': 'optional',
                                      'predicate': rdflib.term.URIRef(
                                          'http://dcat-ap.de/def/dcatde/1_0originator'),  # noqa: E501
                                      'type': None},
                'dcatde_maintainer': {'object': StructRDFSLiteral,
                                      'importance': 'optional',
                                      'predicate': rdflib.term.URIRef(
                                          'http://dcat-ap.de/def/dcatde/1_0maintainer'),  # noqa: E501
                                      'type': None},
                'dct_issued': {'object': StructRDFSLiteral,
                               'importance': 'optional',
                               'predicate': rdflib.term.URIRef(
                                   'http://purl.org/dc/terms/issued'),
                               'type': datetime.date},
                'dct_modified': {'object': StructRDFSLiteral,
                                 'importance': 'optional',
                                 'predicate': rdflib.term.URIRef(
                                     'http://purl.org/dc/terms/modified'),
                                 'type': datetime.date},
                'dcatde_contributorID': {'object': StructRDFSLiteral,
                                         'importance': 'optional',
                                         'predicate': rdflib.term.URIRef(
                                             'http://dcat-ap.de/def/dcatde/1_0contributorID'),  # noqa: E501
                                         'type': dict},
                'dcatde_politicalGeocodingURI': {'object': StructRDFSLiteral,
                                                 'importance': 'optional',
                                                 'predicate': rdflib.term.URIRef(  # noqa: E501
                                                     'http://dcat-ap.de/def/dcatde/1_0politicalGeocodingURI'),
                                                 # noqa: E501
                                                 'type': str},
                'dcatde_politicalGeocodingLevelURI': {'object': StructRDFSLiteral,  # noqa: E501
                                                      'importance': 'optional',
                                                      'predicate': rdflib.term.URIRef(  # noqa: E501
                                                          'http://dcat-ap.de/def/dcatde/1_0politicalGeocodingLevelURI'),
                                                      # noqa: E501
                                                      'type': str},
                'dcatde_geocodingText': {'object': StructRDFSLiteral,
                                         'importance': 'optional',
                                         'predicate': rdflib.term.URIRef(
                                             'http://dcat-ap.de/def/dcatde/1_0geocodingText'),  # noqa: E501
                                         'type': dict},
                'dct_accessRights': {'object': StructRDFSLiteral,
                                     'importance': 'optional',
                                     'predicate': rdflib.term.URIRef(
                                         'http://purl.org/dc/terms/accessRights'),  # noqa: E501
                                     'type': None},
                'owl_versionInfo': {'object': StructRDFSLiteral,
                                    'importance': 'optional',
                                    'predicate': rdflib.term.URIRef('https://www.w3.org/2002/07/owl#versionInfo'),
                                    'type': dict},
                'dcatde_legalbasisText': {'object': StructRDFSLiteral,
                                          'importance': 'optional',
                                          'predicate': rdflib.term.URIRef(
                                              'http://dcat-ap.de/def/dcatde/1_0legalbasisText'),  # noqa: E501
                                          'type': dict},
                'adms_versionNotes': {'object': StructRDFSLiteral,
                                      'importance': 'optional',
                                      'predicate': rdflib.term.URIRef(
                                          'http://www.w3.org/ns/adms#versionNotes'),  # noqa: E501
                                      'type': dict},
                'dcat_landingpage': {'object': StructRDFSLiteral,
                                     'importance': 'optional',
                                     'predicate': rdflib.term.URIRef(
                                         'http://www.w3.org/ns/dcat#landingpage'),  # noqa: E501
                                     'type': str},
                'foaf_page': {'object': StructRDFSLiteral,
                              'importance': 'optional',
                              'predicate': rdflib.term.URIRef(
                                  'http://xmlns.com/foaf/0.1/page'),
                              'type': str},
                'subjects': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://www.w3.org/ns/dcat#keyword'),
                             'type': list},
                'language': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://purl.org/dc/terms/language'),
                             'type': None},
                'subject': {'object': StructRDFSLiteral,
                            'importance': 'optional',
                            'predicate': rdflib.term.URIRef(
                                'http://www.w3.org/ns/dcat#keyword'),
                            'type': list,
                            'rdf_name': 'dcat_keyword'}}

    @property
    def contained(self):
        """Return all contained items.

        :return:
        """
        result = {}
        result['dcat_distribution'] = {
            'object': StructDCATDistribution,
            'importance': IMP_REQUIRED,
            'type': list,
            'predicate': DCAT.distribution,
            'target': DCAT.Distribution,
        }
        return result

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        related = {}
        related['dct_publisher'] = {
            'object': StructFOAFAgent,
            'importance': IMP_OPTIONAL,
            'type': str,
            'predicate': DCT.publisher,
            'target': FOAF.Agent,
        }
        related['dct_rights'] = {
            'object': StructDCTRightsStatement,
            'importance': IMP_OPTIONAL,
            'type': str,
            'predicate': DCT.accessRights,
            'target': DCT.RightsStatement,
        }
        related['dct_spatial'] = {
            'object': StructDCTLocation,
            'importance': IMP_OPTIONAL,
            'type': list,
            'predicate': DCT.spatial,
            'target': DCT.Location,
        }
        related['dcat_theme'] = {
            'object': StructSKOSConcept,
            'importance': IMP_RECOMENDED,
            'type': list,
            'predicate': DCAT.theme,
            'target': SKOS.Concept,
        }
        related['dcat_contactPoint'] = {'object': StructVCARDKind,
                                        'importance': 'optional',
                                        'type': list,
                                        'predicate': rdflib.term.URIRef(
                                            'http://www.w3.org/ns/dcat#contactPoint'), 'type': list,
                                        'target': VCARD.Kind,
                                        }
        return related


@implementer(IStructure)
@adapter(IDCATDistribution)
class StructDCATDistribution(StructBase):
    portal_type = CT_DCAT_DISTRIBUTION
    rdf_type = DCAT.Distribution
    title_field = [
        'dct_title',
        'dcat_accessURL',
    ]

    @property
    def properties(self):
        return {'dct_title': {'object': StructRDFSLiteral,
                              'importance': 'optional',
                              'predicate': rdflib.term.URIRef(
                                  'http://purl.org/dc/terms/title'),
                              'type': dict},
                'dct_description': {'object': StructRDFSLiteral,
                                    'importance': 'optional',
                                    'predicate': rdflib.term.URIRef(
                                        'http://purl.org/dc/terms/description'),  # noqa: E501
                                    'type': dict},
                # changed from optional to required
                'dcat_accessURL': {'object': StructRDFSLiteral,
                                   'importance': 'required',
                                   'predicate': rdflib.term.URIRef(
                                       'http://www.w3.org/ns/dcat#accessURL'),
                                   'type': str},
                'dcat_downloadURL': {'object': StructRDFSLiteral,
                                     'importance': 'optional',
                                     'predicate': rdflib.term.URIRef(
                                         'http://www.w3.org/ns/dcat#downloadURL'),  # noqa: E501
                                     'type': str},
                'dcatde_plannedAvailability': {'object': StructRDFSLiteral,
                                               'importance': 'optional',
                                               'predicate': rdflib.term.URIRef(
                                                   'http://dcat-ap.de/def/dcatde/1_0plannedAvailability'),  # noqa: E501
                                               'type': dict},
                'dcatde_licenseAttributionByText': {'object': StructRDFSLiteral,  # noqa: E501
                                                    'importance': 'optional',
                                                    'predicate': rdflib.term.URIRef(  # noqa: E501
                                                        'http://dcat-ap.de/def/dcatde/1_0licenseAttributionByText'),
                                                    # noqa: E501
                                                    'type': dict},
                'dcat_byteSize': {'object': StructRDFSLiteral,
                                  'importance': 'optional',
                                  'predicate': rdflib.term.URIRef(
                                      'http://www.w3.org/ns/dcat#byteSize'),
                                  'type': dict},
                'dct_issued': {'object': StructRDFSLiteral,
                               'importance': 'optional',
                               'predicate': rdflib.term.URIRef(
                                   'http://purl.org/dc/terms/issued'),
                               'type': datetime.date},
                'dct_modified': {'object': StructRDFSLiteral,
                                 'importance': 'optional',
                                 'predicate': rdflib.term.URIRef(
                                     'http://purl.org/dc/terms/modified'),
                                 'type': datetime.date},
                'dct_identifier': {'object': StructRDFSLiteral,
                                   'importance': 'optional',
                                   'predicate': rdflib.term.URIRef(
                                       'http://purl.org/dc/terms/identifier'),
                                   'type': str},
                'adms_identifier': {'object': StructRDFSLiteral,
                                    'importance': 'optional',
                                    'predicate': rdflib.term.URIRef(
                                        'http://www.w3.org/ns/adms#identifier'),  # noqa: E501
                                    'type': str},
                'subjects': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://www.w3.org/ns/dcat#keyword'),
                             'type': list},
                'language': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://purl.org/dc/terms/language'),
                             'type': None},
                'subject': {'object': StructRDFSLiteral,
                            'importance': 'optional',
                            'predicate': rdflib.term.URIRef(
                                'http://www.w3.org/ns/dcat#keyword'),
                            'type': list, 'rdf_name': 'dcat_keyword'}}

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        related = {}
        related['dct_license'] = {
            'object': StructDCTLicenseDocument,
            'importance': IMP_OPTIONAL,
            'type': str,
            'predicate': DCT.license,
            'target': DCT.LicenseDocument,
        }
        related['dct_format'] = {
            'object': StructDCTMediaTypeOrExtent,
            'importance': IMP_OPTIONAL,
            'type': str,
            # Hack since format is buildin
            'predicate': rdflib.term.URIRef(str(DCT) + u'format'),
            'target': DCT.MediaTypeOrExtent,
        }
        related['dcat_mediaType'] = {
            'object': StructDCTMediaTypeOrExtent,
            'importance': IMP_OPTIONAL,
            'type': str,
            'predicate': DCAT.mediaType,
            'target': DCT.MediaTypeOrExtent,
        }
        related['dct_conformsTo'] = {
            'object': StructDCTStandard,
            'importance': IMP_OPTIONAL,
            'type': list,
            'predicate': DCT.conformsTo,
            'target': DCT.Standard,
        }
        related['dct_rights'] = {
            'object': StructDCTRightsStatement,
            'importance': IMP_OPTIONAL,
            'type': str,
            'predicate': DCT.rights,
            'target': DCT.RightsStatement,
        }
        return related


@implementer(IStructure)
@adapter(IDCTLicenseDocument)
class StructDCTLicenseDocument(StructBase):
    """Structure definition of dct:licenseDocument"""

    portal_type = CT_DCT_LICENSEDOCUMENT
    rdf_type = DCT.LicenseDocument

    @property
    def properties(self):
        return {
            # changed from required to optional
            'dct_title': {'object': StructRDFSLiteral,
                          'importance': 'optional',
                          'predicate': rdflib.term.URIRef(
                              'http://purl.org/dc/terms/title'),
                          'type': dict},
            'dct_description': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://purl.org/dc/terms/description'),
                                'type': dict},
            'rdfs_isDefinedBy': {'object': StructRDFSLiteral,
                                 'importance': 'optional',
                                 'predicate': rdflib.term.URIRef(
                                     'http://www.w3.org/2000/01/rdf-schema#isDefinedBy'),  # noqa: E501
                                 'type': str},
            'dct_identifier': {'object': StructRDFSLiteral,
                               'importance': 'optional',
                               'predicate': rdflib.term.URIRef(
                                   'http://purl.org/dc/terms/identifier'),
                               'type': str},
            'adms_identifier': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://www.w3.org/ns/adms#identifier'),
                                'type': str},
            'subjects': {'object': StructRDFSLiteral,
                         'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://www.w3.org/ns/dcat#keyword'),
                         'type': list},
            'language': {'object': StructRDFSLiteral,
                         'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://purl.org/dc/terms/language'),
                         'type': None},
            'subject': {'object': StructRDFSLiteral,
                        'importance': 'optional',
                        'predicate': rdflib.term.URIRef(
                            'http://www.w3.org/ns/dcat#keyword'),
                        'type': list, 'rdf_name': 'dcat_keyword'}}


@implementer(IStructure)
@adapter(IDCTLocation)
class StructDCTLocation(StructBase):
    """Structure definition of dct:Location"""

    portal_type = CT_DCT_LOCATION
    rdf_type = DCT.Location

    @property
    def properties(self):
        return {
            # changed from required to optional
            'dct_title': {'object': StructRDFSLiteral,
                          'importance': 'optional',
                          'predicate': rdflib.term.URIRef(
                              'http://purl.org/dc/terms/title'),
                          'type': dict},
            'dct_description': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://purl.org/dc/terms/description'),
                                'type': dict},
            'rdfs_isDefinedBy': {'object': StructRDFSLiteral,
                                 'importance': 'optional',
                                 'predicate': rdflib.term.URIRef(
                                     'http://www.w3.org/2000/01/rdf-schema#isDefinedBy'),  # noqa: E501
                                 'type': str},
            'dct_identifier': {'object': StructRDFSLiteral,
                               'importance': 'optional',
                               'predicate': rdflib.term.URIRef(
                                   'http://purl.org/dc/terms/identifier'),
                               'type': str},
            'adms_identifier': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://www.w3.org/ns/adms#identifier'),
                                'type': str},
            'subjects': {'object': StructRDFSLiteral,
                         'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://www.w3.org/ns/dcat#keyword'),
                         'type': list},
            'language': {'object': StructRDFSLiteral,
                         'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://purl.org/dc/terms/language'),
                         'type': None},
            'subject': {'object': StructRDFSLiteral,
                        'importance': 'optional',
                        'predicate': rdflib.term.URIRef(
                            'http://www.w3.org/ns/dcat#keyword'),
                        'type': list,
                        'rdf_name': 'dcat_keyword'}}


@implementer(IStructure)
@adapter(IDCTLanguage)
class StructDCTLanguage(StructBase):
    """Structure definition of dct:Language"""

    portal_type = CT_DCT_LANGUAGE
    rdf_type = DCT.language

    @property
    def properties(self):
        return {
            # changed from required to optional
            'dct_title': {'object': StructRDFSLiteral,
                          'importance': 'optional',
                          'predicate': rdflib.term.URIRef(
                              'http://purl.org/dc/terms/title'),
                          'type': dict},
            'dct_description': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://purl.org/dc/terms/description'),
                                'type': dict},
            'rdfs_isDefinedBy': {'object': StructRDFSLiteral,
                                 'importance': 'optional',
                                 'predicate': rdflib.term.URIRef(
                                     'http://www.w3.org/2000/01/rdf-schema#isDefinedBy'),  # noqa: E501
                                 'type': str},
            # 'old_representation': {'object': StructRDFSLiteral,
            #                        'importance': 'optional',
            #                        'predicate': 'old_representation',
            #                        'type': str},
            # # changed from required to optional
            # 'new_representation': {'object': StructRDFSLiteral,
            #                        'importance': 'optional',
            #                        'predicate': 'new_representation',
            #                        'type': str},
            'dct_identifier': {'object': StructRDFSLiteral,
                               'importance': 'optional',
                               'predicate': rdflib.term.URIRef(
                                   'http://purl.org/dc/terms/identifier'),
                               'type': str},
            'adms_identifier': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://www.w3.org/ns/adms#identifier'),
                                'type': str},
            'subjects': {'object': StructRDFSLiteral,
                         'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://www.w3.org/ns/dcat#keyword'),
                         'type': list},
            'language': {'object': StructRDFSLiteral,
                         'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://purl.org/dc/terms/language'),
                         'type': None},
            'subject': {'object': StructRDFSLiteral,
                        'importance': 'optional',
                        'predicate': rdflib.term.URIRef(
                            'http://www.w3.org/ns/dcat#keyword'),
                        'type': list,
                        'rdf_name': 'dcat_keyword'}}


@implementer(IStructure)
@adapter(IDCTMediaTypeOrExtent)
class StructDCTMediaTypeOrExtent(StructBase):
    """Structure definition of dct:Mediatypeorextent"""

    portal_type = CT_DCT_MEDIATYPEOREXTENT
    rdf_type = DCT.MediaTypeOrExtent

    literal_field = None

    # This is a hack to fullfill Convention 31
    title_field = ['rdf_about']

    _not_required = ['dct_title']

    @property
    def properties(self):
        return {'dct_title': {'object': StructRDFSLiteral,
                              'importance': 'optional',
                              'predicate': rdflib.term.URIRef(
                                  'http://purl.org/dc/terms/title'),
                              'type': dict},
                'dct_description': {'object': StructRDFSLiteral,
                                    'importance': 'optional',
                                    'predicate': rdflib.term.URIRef(
                                        'http://purl.org/dc/terms/description'),  # noqa: E501
                                    'type': dict},
                'rdfs_isDefinedBy': {'object': StructRDFSLiteral,
                                     'importance': 'optional',
                                     'predicate': rdflib.term.URIRef(
                                         'http://www.w3.org/2000/01/rdf-schema#isDefinedBy'),  # noqa: E501
                                     'type': str},
                'dct_identifier': {'object': StructRDFSLiteral,
                                   'importance': 'optional',
                                   'predicate': rdflib.term.URIRef(
                                       'http://purl.org/dc/terms/identifier'),
                                   'type': str},
                'adms_identifier': {'object': StructRDFSLiteral,
                                    'importance': 'optional',
                                    'predicate': rdflib.term.URIRef(
                                        'http://www.w3.org/ns/adms#identifier'),  # noqa: E501
                                    'type': str},
                'subjects': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://www.w3.org/ns/dcat#keyword'),
                             'type': list},
                'language': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://purl.org/dc/terms/language'),
                             'type': None},
                'subject': {'object': StructRDFSLiteral,
                            'importance': 'optional',
                            'predicate': rdflib.term.URIRef(
                                'http://www.w3.org/ns/dcat#keyword'),
                            'type': list,
                            'rdf_name': 'dcat_keyword'}}


@implementer(IStructure)
@adapter(IDCTStandard)
class StructDCTStandard(StructBase):
    """Structure definition of dct:Standard"""

    portal_type = CT_DCT_STANDARD
    rdf_type = DCT.Standard

    @property
    def properties(self):
        return {
            # changed from required to optional
            'dct_title': {'object': StructRDFSLiteral,
                          'importance': 'optional',
                          'predicate': rdflib.term.URIRef(
                              'http://purl.org/dc/terms/title'),
                          'type': dict},
            'dct_description': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://purl.org/dc/terms/description'),
                                'type': dict},
            'rdfs_isDefinedBy': {'object': StructRDFSLiteral,
                                 'importance': 'optional',
                                 'predicate': rdflib.term.URIRef(
                                     'http://www.w3.org/2000/01/rdf-schema#isDefinedBy'),  # noqa: E501
                                 'type': str},
            'dct_identifier': {'object': StructRDFSLiteral,
                               'importance': 'optional',
                               'predicate': rdflib.term.URIRef(
                                   'http://purl.org/dc/terms/identifier'),
                               'type': str},
            'adms_identifier': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://www.w3.org/ns/adms#identifier'),
                                'type': str},
            'subjects': {'object': StructRDFSLiteral, 'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://www.w3.org/ns/dcat#keyword'),
                         'type': list},
            'language': {'object': StructRDFSLiteral, 'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://purl.org/dc/terms/language'),
                         'type': None},
            'subject': {'object': StructRDFSLiteral, 'importance': 'optional',
                        'predicate': rdflib.term.URIRef(
                            'http://www.w3.org/ns/dcat#keyword'), 'type': list,
                        'rdf_name': 'dcat_keyword'}}


@implementer(IStructure)
@adapter(IDCTRightsStatement)
class StructDCTRightsStatement(StructBase):
    """Structure definition of dct:RightsStatement"""

    portal_type = CT_DCT_RIGHTSSTATEMENT
    rdf_type = DCT.RightsStatement

    @property
    def properties(self):
        return {
            # changed from required to optional
            'dct_title': {'object': StructRDFSLiteral,
                          'importance': 'optional',
                          'predicate': rdflib.term.URIRef(
                              'http://purl.org/dc/terms/title'), 'type': dict},
            'dct_description': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://purl.org/dc/terms/description'),
                                'type': dict},
            'rdfs_isDefinedBy': {'object': StructRDFSLiteral,
                                 'importance': 'optional',
                                 'predicate': rdflib.term.URIRef(
                                     'http://www.w3.org/2000/01/rdf-schema#isDefinedBy'),  # noqa: E501
                                 'type': str},
            'dct_identifier': {'object': StructRDFSLiteral,
                               'importance': 'optional',
                               'predicate': rdflib.term.URIRef(
                                   'http://purl.org/dc/terms/identifier'),
                               'type': str},
            'adms_identifier': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://www.w3.org/ns/adms#identifier'),
                                'type': str},
            'subjects': {'object': StructRDFSLiteral,
                         'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://www.w3.org/ns/dcat#keyword'),
                         'type': list},
            'language': {'object': StructRDFSLiteral,
                         'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://purl.org/dc/terms/language'),
                         'type': None},
            'subject': {'object': StructRDFSLiteral,
                        'importance': 'optional',
                        'predicate': rdflib.term.URIRef(
                            'http://www.w3.org/ns/dcat#keyword'),
                        'type': list,
                        'rdf_name': 'dcat_keyword'}}


@implementer(IStructure)
@adapter(IFOAFAgent)
class StructFOAFAgent(StructBase):
    """Structure definition of foaf:Agent"""

    portal_type = CT_FOAF_AGENT
    rdf_type = FOAF.Agent
    title_field = ['foaf_name']

    @property
    def properties(self):
        return {'foaf_name': {'object': StructRDFSLiteral,
                              'importance': 'required',
                              'predicate': rdflib.term.URIRef(
                                  'http://xmlns.com/foaf/0.1/name'),
                              'type': dict},
                'dct_description': {'object': StructRDFSLiteral,
                                    'importance': 'optional',
                                    'predicate': rdflib.term.URIRef(
                                        'http://purl.org/dc/terms/description'),  # noqa: E501
                                    'type': dict},
                'rdfs_isDefinedBy': {'object': StructRDFSLiteral,
                                     'importance': 'optional',
                                     'predicate': rdflib.term.URIRef(
                                         'http://www.w3.org/2000/01/rdf-schema#isDefinedBy'),  # noqa: E501
                                     'type': str},
                'dct_identifier': {'object': StructRDFSLiteral,
                                   'importance': 'optional',
                                   'predicate': rdflib.term.URIRef(
                                       'http://purl.org/dc/terms/identifier'),
                                   'type': str},
                'adms_identifier': {'object': StructRDFSLiteral,
                                    'importance': 'optional',
                                    'predicate': rdflib.term.URIRef(
                                        'http://www.w3.org/ns/adms#identifier'),  # noqa: E501
                                    'type': str},
                'subjects': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://www.w3.org/ns/dcat#keyword'),
                             'type': list},
                'language': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://purl.org/dc/terms/language'),
                             'type': None},
                'subject': {'object': StructRDFSLiteral,
                            'importance': 'optional',
                            'predicate': rdflib.term.URIRef(
                                'http://www.w3.org/ns/dcat#keyword'),
                            'type': list,
                            'rdf_name': 'dcat_keyword'}}


@implementer(IStructure)
@adapter(ISKOSConceptScheme)
class StructSKOSConceptScheme(StructBase):
    """Structure definition of skos:ConceptScheme"""

    portal_type = CT_SKOS_CONCEPTSCHEME
    rdf_type = SKOS.ConceptScheme

    @property
    def contained(self):
        """Return all contained items.

        :return:
        """
        result = {}
        result['skos_concept'] = {
            'object': StructSKOSConcept,
            'importance': IMP_OPTIONAL,
            'type': list,
            'predicate': SKOS.member,
            'target': SKOS.Concept,
        }
        return result

    @property
    def properties(self):
        return {'dct_title': {'object': StructRDFSLiteral,
                              'importance': 'required',
                              'predicate': rdflib.term.URIRef(
                                  'http://purl.org/dc/terms/title'),
                              'type': dict},
                'dct_description': {'object': StructRDFSLiteral,
                                    'importance': 'optional',
                                    'predicate': rdflib.term.URIRef(
                                        'http://purl.org/dc/terms/description'),  # noqa: E501
                                    'type': dict},
                # changed from required to optional
                'skos_inScheme': {'object': StructRDFSLiteral,
                                  'importance': 'optional',
                                  'predicate': rdflib.term.URIRef(
                                      'http://www.w3.org/2004/02/skos/core#inScheme'),  # noqa: E501
                                  'type': str},
                'rdfs_isDefinedBy': {'object': StructRDFSLiteral,
                                     'importance': 'optional',
                                     'predicate': rdflib.term.URIRef(
                                         'http://www.w3.org/2000/01/rdf-schema#isDefinedBy'),  # noqa: E501
                                     'type': str},
                'foaf_depiction': {'object': StructRDFSLiteral,
                                   'importance': 'optional',
                                   'predicate': rdflib.term.URIRef(
                                       'http://xmlns.com/foaf/0.1/depiction'),
                                   'type': str},
                'dct_identifier': {'object': StructRDFSLiteral,
                                   'importance': 'optional',
                                   'predicate': rdflib.term.URIRef(
                                       'http://purl.org/dc/terms/identifier'),
                                   'type': str},
                'adms_identifier': {'object': StructRDFSLiteral,
                                    'importance': 'optional',
                                    'predicate': rdflib.term.URIRef(
                                        'http://www.w3.org/ns/adms#identifier'),  # noqa: E501
                                    'type': str},
                'subjects': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://www.w3.org/ns/dcat#keyword'),
                             'type': list},
                'language': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://purl.org/dc/terms/language'),
                             'type': None},
                'subject': {'object': StructRDFSLiteral,
                            'importance': 'optional',
                            'predicate': rdflib.term.URIRef(
                                'http://www.w3.org/ns/dcat#keyword'),
                            'type': list,
                            'rdf_name': 'dcat_keyword'}}


@implementer(IStructure)
@adapter(IVCARDKind)
class StructVCARDKind(StructBase):
    """Structure definition of vcard:Kind"""

    portal_type = CT_VCARD_KIND
    rdf_type = VCARD.Kind
    title_field = ['vcard_fn']

    @property
    def properties(self):
        return {
            # changed from required to optional
            'vcard_fn': {'object': StructRDFSLiteral,
                         'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://www.w3.org/2006/vcard/ns#fn'),
                         'type': dict},
            # changed from required to optional
            'dct_description': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://purl.org/dc/terms/description'),
                                'type': dict},
            'vcard_hasEmail': {'object': StructRDFSLiteral,
                               'importance': 'optional',
                               'predicate': rdflib.term.URIRef(
                                   'http://www.w3.org/2006/vcard/ns#hasEmail'),
                               'type': list},
            'vcard_hasTelephone': {'object': StructRDFSLiteral,
                                   'importance': 'optional',
                                   'predicate': rdflib.term.URIRef(
                                       'http://www.w3.org/2006/vcard/ns#hasTelephone'),  # noqa: E501
                                   'type': list},
            'vcard_hasURL': {'object': StructRDFSLiteral,
                             'importance': 'optional',
                             'predicate': rdflib.term.URIRef(
                                 'http://www.w3.org/2006/vcard/ns#hasURL'),
                             'type': str},
            'vcard_Fax': {'object': StructRDFSLiteral,
                          'importance': 'optional',
                          'predicate': rdflib.term.URIRef(
                              'http://www.w3.org/2006/vcard/ns#Fax'),
                          'type': list},
            'dct_identifier': {'object': StructRDFSLiteral,
                               'importance': 'optional',
                               'predicate': rdflib.term.URIRef(
                                   'http://purl.org/dc/terms/identifier'),
                               'type': str},
            'adms_identifier': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://www.w3.org/ns/adms#identifier'),
                                'type': str},
            'subjects': {'object': StructRDFSLiteral, 'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://www.w3.org/ns/dcat#keyword'),
                         'type': list},
            'language': {'object': StructRDFSLiteral, 'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://purl.org/dc/terms/language'),
                         'type': None},
            'subject': {'object': StructRDFSLiteral, 'importance': 'optional',
                        'predicate': rdflib.term.URIRef(
                            'http://www.w3.org/ns/dcat#keyword'), 'type': list,
                        'rdf_name': 'dcat_keyword'}}


@implementer(IStructure)
@adapter(ISKOSConcept)
class StructSKOSConcept(StructBase):
    """Structure definition of skos:Concept"""

    portal_type = CT_SKOS_CONCEPT
    rdf_type = SKOS.Concept

    @property
    def properties(self):
        return {
            # missing: Required skos:PrefLabel instead of dct_title
            # dct_title should be optional, skos:PrefLabel required
            'dct_title': {'object': StructRDFSLiteral,
                          'importance': 'required',
                          'predicate': rdflib.term.URIRef(
                              'http://purl.org/dc/terms/title'),
                          'type': dict},
            'dct_description': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://purl.org/dc/terms/description'),
                                'type': dict},
            # changed from required to optional
            'skos_inScheme': {'object': StructRDFSLiteral,
                              'importance': 'optional',
                              'predicate': rdflib.term.URIRef(
                                  'http://www.w3.org/2004/02/skos/core#inScheme'),  # noqa: E501
                              'type': str},
            'rdfs_isDefinedBy': {'object': StructRDFSLiteral,
                                 'importance': 'optional',
                                 'predicate': rdflib.term.URIRef(
                                     'http://www.w3.org/2000/01/rdf-schema#isDefinedBy'),  # noqa: E501
                                 'type': str},
            'foaf_depiction': {'object': StructRDFSLiteral,
                               'importance': 'optional',
                               'predicate': rdflib.term.URIRef(
                                   'http://xmlns.com/foaf/0.1/depiction'),
                               'type': str},
            'dct_identifier': {'object': StructRDFSLiteral,
                               'importance': 'optional',
                               'predicate': rdflib.term.URIRef(
                                   'http://purl.org/dc/terms/identifier'),
                               'type': str},
            'adms_identifier': {'object': StructRDFSLiteral,
                                'importance': 'optional',
                                'predicate': rdflib.term.URIRef(
                                    'http://www.w3.org/ns/adms#identifier'),
                                'type': str},
            'subjects': {'object': StructRDFSLiteral, 'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://www.w3.org/ns/dcat#keyword'),
                         'type': list},
            'language': {'object': StructRDFSLiteral, 'importance': 'optional',
                         'predicate': rdflib.term.URIRef(
                             'http://purl.org/dc/terms/language'),
                         'type': None},
            'subject': {'object': StructRDFSLiteral, 'importance': 'optional',
                        'predicate': rdflib.term.URIRef(
                            'http://www.w3.org/ns/dcat#keyword'), 'type': list,
                        'rdf_name': 'dcat_keyword'}}


@implementer(IStructure)
@adapter(IRDFSLiteral)
class StructRDFSLiteral(StructBase):
    """Structure definition of skos:Concept"""

    portal_type = CT_RDFS_LITERAL
    rdf_type = RDFS.Literal


STRUCTURES = [
    StructRDFSLiteral,
    StructSKOSConcept,
    StructVCARDKind,
    StructSKOSConceptScheme,
    StructFOAFAgent,
    StructDCTRightsStatement,
    StructDCTStandard,
    StructDCTMediaTypeOrExtent,
    StructDCTLanguage,
    StructDCTLocation,
    StructDCTLicenseDocument,
    StructDCATDistribution,
    StructDCATCatalog,
    StructDCATDataset,
]

STRUCT_BY_NS_CLASS = {
    i.rdf_type: i for i in STRUCTURES
}

STRUCT_BY_PORTAL_TYPE = {
    i.portal_type: i for i in STRUCTURES
}
