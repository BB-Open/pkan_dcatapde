# -*- coding: utf-8 -*-
"""Structure of the dcat-AP.de scheme"""
import rdflib
from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DCAT_CATALOG, FIELD_BLACKLIST
from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.constants import CT_DCAT_DISTRIBUTION
from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.constants import CT_DCT_LOCATION
from pkan.dcatapde.constants import CT_DCT_MEDIATYPEOREXTENT
from pkan.dcatapde.constants import CT_DCT_RIGHTSSTATEMENT
from pkan.dcatapde.constants import CT_DCT_STANDARD
from pkan.dcatapde.constants import CT_FOAF_AGENT
from pkan.dcatapde.constants import CT_RDF_LITERAL
from pkan.dcatapde.constants import CT_SKOS_CONCEPT
from pkan.dcatapde.constants import CT_SKOS_CONCEPTSCHEME
from pkan.dcatapde.content.dcat_catalog import IDCATCatalog
from pkan.dcatapde.content.dcat_dataset import IDCATDataset
from pkan.dcatapde.content.dcat_distribution import IDCATDistribution
from pkan.dcatapde.content.dct_licensedocument import IDCTLicenseDocument
from pkan.dcatapde.content.dct_location import IDCTLocation
from pkan.dcatapde.content.dct_mediatypeorextent import IDCTMediaTypeOrExtent
from pkan.dcatapde.content.dct_rightsstatement import IDCTRightsStatement
from pkan.dcatapde.content.dct_standard import IDCTStandard
from pkan.dcatapde.content.foaf_agent import IFOAFAgent
from pkan.dcatapde.content.skos_concept import ISKOSConcept
from pkan.dcatapde.content.skos_conceptscheme import ISKOSConceptScheme
from pkan.dcatapde.structure.interfaces import IStructure
from pkan.dcatapde.structure.sparql import DCT, DCAT, INIT_NS
from plone.api import portal
from plone.api.portal import get_current_language
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from plone.supermodel.interfaces import FIELDSETS_KEY
from rdflib.namespace import FOAF, SKOS
from zope.component import adapter
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer

from zope.schema import getFieldsInOrder
from zope.schema.vocabulary import SimpleTerm


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
    title_field = 'dct_title'

    # caching
    _fields_in_order = None
    _fields_objects_required = {}

    _blacklist = FIELD_BLACKLIST

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
        for field_name, field in self.fields_in_order:
            if field_name in self._blacklist:
                continue

            result[field_name] = {
                'object': CT_RDF_LITERAL,
                'required': field.required,
                'predicate': self.fieldname2predicate(field_name),
                'type': field._type
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

    @property
    def vocab_terms(self):
        """Terms for a vocabulary. The tokens hold the subjects CT,
        and the predicate. The objects type information is neglected."""

        field_names = self.fields_objects_required.keys()
        field_names.sort()

        terms = []
        for field_name in field_names:
            required = self.fields_objects_required[field_name]['required']
            if required:
                title = _(
                    u'${CT}=>${field_name} (required)',
                    mapping={
                        u'field_name': u'{0}'.format(field_name),
                        u'CT': u'{0}'.format(self.portal_type),
                    },
                )
                token = '{CT}__{field_name}__required'.format(
                    CT=self.portal_type,
                    field_name=field_name,
                )
            else:
                title = _(
                    u'${CT}=>${field_name}',
                    mapping={
                        u'field_name': u'{0}'.format(field_name),
                        u'CT': u'{0}'.format(self.portal_type),
                    },
                )
                token = '{CT}__{field_name}'.format(
                    CT=self.portal_type,
                    field_name=field_name,
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


@implementer(IStructure)
@adapter(IDCATCatalog)
class StructDCATCatalog(StructBase):
    """Structure definition of foafdcat:Catalog"""

    portal_type = CT_DCAT_CATALOG
    rdf_type = DCAT.Catalog

    @property
    def contained(self):
        """Return all contained items.

        :return:
        """
        result = {}
        result['dcat_dataset'] = {
            'object': StructDCATDataset,
            'required': True,
            'type': list,
            'predicate': DCAT.dataset,
            'target': DCT.Dataset,
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
            'required': True,
            'type': str,
            'predicate': DCT.publisher,
            'target': FOAF.Agent,
        }
        related['dct_license'] = {
            'object': StructDCTLicenseDocument,
            'required': False,
            'type': str,
            'predicate': DCT.license,
            'target': DCT.LicenseDocument,
        }
        related['dct_rights'] = {
            'object': StructDCTRightsstatement,
            'required': False,
            'type': str,
            'predicate': DCT.rights,
            'target': DCT.RightsStatement,
        }
        related['dct_spatial'] = {
            'object': StructDCTLocation,
            'required': False,
            'type': list,
            'predicate': DCT.spatial,
            'target': DCT.Location,
        }
        return related


@implementer(IStructure)
@adapter(IDCATDataset)
class StructDCATDataset(StructBase):

    portal_type = CT_DCAT_DATASET
    rdf_type = DCAT.Dataset

    @property
    def contained(self):
        """Return all contained items.

        :return:
        """
        result = {}
        result['dcat_distribution'] = {
            'object': StructDCATDistribution,
            'required': True,
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
            'required': False,
            'type': str,
            'predicate': DCT.publisher,
            'target': FOAF.Agent,
        }
        related['dct_rights'] = {
            'object': StructDCTRightsstatement,
            'required': False,
            'type': str,
            'predicate': DCT.accessRights,
            'target': DCT.RightsStatement,
        }
        related['dct_spatial'] = {
            'object': StructDCTLocation,
            'required': False,
            'type': list,
            'predicate': DCT.spatial,
            'target': DCT.Location,
        }
        return related


@implementer(IStructure)
@adapter(IDCATDistribution)
class StructDCATDistribution(StructBase):

    portal_type = CT_DCAT_DISTRIBUTION
    rdf_type = DCAT.Distribution

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        related = {}
        related['dct_license'] = {
            'object': StructDCTLicenseDocument,
            'required': False,
            'type': str,
            'predicate': DCT.license,
            'target': DCT.LicenseDocument,
        }
        related['dct_format'] = {
            'object': StructDCTMediaTypeOrExtent,
            'required': False,
            'type': str,
            'predicate': DCT.format,
            'target': DCT.MediaTypeOrExtent,
        }
        related['dct_mediaType'] = {
            'object': StructDCTMediaTypeOrExtent,
            'required': False,
            'type': str,
            'predicate': DCT.mediatype,
            'target': DCT.MediaTypeOrExtent,
        }
        related['dct_conformsTo'] = {
            'object': StructDCTStandard,
            'required': False,
            'type': list,
            'predicate': DCT.conformsTo,
            'target': DCT.Standard,
        }
        related['dct_rights'] = {
            'object': StructDCTRightsstatement,
            'required': False,
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


@implementer(IStructure)
@adapter(IDCTLocation)
class StructDCTLocation(StructBase):
    """Structure definition of dct:Location"""

    portal_type = CT_DCT_LOCATION
    rdf_type = DCT.Location


@implementer(IStructure)
@adapter(IDCTMediaTypeOrExtent)
class StructDCTMediaTypeOrExtent(StructBase):
    """Structure definition of dct:Mediatypeorextent"""

    portal_type = CT_DCT_MEDIATYPEOREXTENT
    rdf_type = DCT.MediaTypeOrExtent


@implementer(IStructure)
@adapter(IDCTStandard)
class StructDCTStandard(StructBase):
    """Structure definition of dct:Standard"""

    portal_type = CT_DCT_STANDARD
    rdf_type = DCT.Standard


@implementer(IStructure)
@adapter(IDCTRightsStatement)
class StructDCTRightsstatement(StructBase):
    """Structure definition of dct:RightsStatement"""

    portal_type = CT_DCT_STANDARD
    rdf_type = DCT.RightsStatement


@implementer(IStructure)
@adapter(IFOAFAgent)
class StructFOAFAgent(StructBase):
    """Structure definition of foaf:Agent"""

    portal_type = CT_FOAF_AGENT
    rdf_type = FOAF.Agent
    title_field = 'foaf_name'

@implementer(IStructure)
@adapter(ISKOSConceptScheme)
class StructSKOSConceptScheme(StructBase):
    """Structure definition of skos:ConceptSchema"""

    portal_type = CT_SKOS_CONCEPTSCHEME
    rdf_type = SKOS.ConceptSchema


@implementer(IStructure)
@adapter(ISKOSConcept)
class StructSKOSConcept(StructBase):
    """Structure definition of skos:Concept"""

    portal_type = CT_SKOS_CONCEPT
    rdf_type = SKOS.Concept
