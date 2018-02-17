# -*- coding: utf-8 -*-
"""Structure of the dcat-AP.de scheme"""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.constants import CT_DCAT_DISTRIBUTION
from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.constants import CT_DCT_LOCATION
from pkan.dcatapde.constants import CT_DCT_MEDIATYPEOREXTENT
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
from pkan.dcatapde.content.dct_standard import IDCTStandard
from pkan.dcatapde.content.foaf_agent import IFOAFAgent
from pkan.dcatapde.content.skos_concept import ISKOSConcept
from pkan.dcatapde.content.skos_conceptscheme import ISKOSConceptScheme
from plone.api import portal
from plone.api.portal import get_current_language
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from plone.supermodel.interfaces import FIELDSETS_KEY
from zope.component import adapter
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
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


class IStructure(Interface):
    """Marker interface for Structure classes"""


@implementer(IStructure)
@adapter(IDexterityFTI)
class StructBase(object):
    """Utility functions for all structure classes"""

    # The content type this structure represents
    portal_type = None

    # caching
    _fields_in_order = None
    _fields_objects_required = {}

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
            # todo: Filter
            result[field_name] = field
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

    @property
    def fields_objects_required(self):
        """Return all predicates, there objects types and if they are
        required"""

        if not self._fields_objects_required:
            self._fields_objects_required = {}
            # First the properties
            for field_name, field in self.properties.items():
                self._fields_objects_required[field_name] = {
                    'object': CT_RDF_LITERAL,
                    'required': field.required,
                }

            # Then the contained
            for field_name in self.contained:
                object_type, required = self.contained[field_name]
                self._fields_objects_required[field_name] = {
                    'object': object_type,
                    'required': True,
                }

            # Then the referenced
            for field_name in self.referenced:
                object_type, required = self.referenced[field_name]
                self._fields_objects_required[field_name] = {
                    'object': object_type,
                    'required': True,
                }

        return self._fields_objects_required

    @property
    def vocab_terms(self):
        """Terms for a vocabulary. The tokens hold the subjects CT,
        and the predicate. The objects type information is neglected."""

        field_names = self.fields_objects_required.keys()
        field_names.sort()

        terms = []
        for field_name in field_names:
            object_type, required = self.fields_objects_required[field_name]
            if required:
                title = _(
                    '{CT} {field_name} (required)',
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
                    '{CT} {field_name}',
                    mapping={
                        u'field_name': u'{0}'.format(field_name),
                        u'CT': u'{0}'.format(self.portal_type),
                    },
                )
                token = '{CT}__{field_name}'.format(
                    CT=self.portal_type,
                    field_name=field_name,
                )

            terms.append(
                SimpleTerm(
                    value=token, token=token, title=translate(
                        title,
                        target_language=get_current_language()),
                ),
            )
        return terms


@implementer(IStructure)
@adapter(IDCATCatalog)
class StructDCATCatalog(StructBase):
    """Structure definition of foafdcat:Catalog"""

    portal_type = CT_DCAT_CATALOG

    @property
    def contained(self):
        """Return all contained items.

        :return:
        """
        result = {}
        result['dcat_dataset'] = {
            'object': CT_DCAT_DISTRIBUTION,
            'required': True,
        }
        return result

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        related = {}
        related['dct_publisher'] = {
            'object': CT_FOAF_AGENT,
            'required': True,
        }
        related['dct_license'] = {
            'object': CT_DCT_LICENSEDOCUMENT,
            'required': False,
        }
        related['dct_spatial'] = {
            'object': CT_DCT_LOCATION,
            'required': False,
        }
        return related


@implementer(IStructure)
@adapter(IDCATDataset)
class StructDCATDataset(StructBase):

    portal_type = CT_DCAT_DATASET

    @property
    def contained(self):
        """Return all contained items.

        :return:
        """
        result = {}
        result['dcat_distribution'] = {
            'object': CT_DCAT_DISTRIBUTION,
            'required': True,
        }
        return result

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        related = {}
        related['dct_publisher'] = {
            'object': CT_FOAF_AGENT,
            'required': False,
        }
        related['dct_license'] = {
            'object': CT_DCT_LICENSEDOCUMENT,
            'required': False,
        }
        related['dct_spatial'] = {
            'object': CT_DCT_LOCATION,
            'required': False,
        }
        return related


@implementer(IStructure)
@adapter(IDCATDistribution)
class StructDCATDistribution(StructBase):

    portal_type = CT_DCAT_DISTRIBUTION

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        related = {}
        related['dct_license'] = {
            'object': CT_DCT_LICENSEDOCUMENT,
            'required': False,
        }
        related['dct_format'] = {
            'object': CT_DCT_MEDIATYPEOREXTENT,
            'required': False,
        }
        related['dct_mediaType'] = {
            'object': CT_DCT_MEDIATYPEOREXTENT,
            'required': False,
        }
        related['dct_conformsTo'] = {
            'object': CT_DCT_STANDARD,
            'required': False,
        }
        return related


@implementer(IStructure)
@adapter(IDCTLicenseDocument)
class StructDCTLicenseDocument(StructBase):
    """Structure definition of dct:licenseDocument"""

    portal_type = CT_DCT_LICENSEDOCUMENT


@implementer(IStructure)
@adapter(IDCTLocation)
class StructDCTLocation(StructBase):
    """Structure definition of dct:Location"""

    portal_type = CT_DCT_LOCATION


@implementer(IStructure)
@adapter(IDCTMediaTypeOrExtent)
class StructDCTMediaTypeOrExtent(StructBase):
    """Structure definition of dct:Mediatypeorextent"""

    portal_type = CT_DCT_MEDIATYPEOREXTENT


@implementer(IStructure)
@adapter(IDCTStandard)
class StructDCTStandard(StructBase):
    """Structure definition of dct:Standard"""

    portal_type = CT_DCT_STANDARD


@implementer(IStructure)
@adapter(IFOAFAgent)
class StructFOAFAgent(StructBase):
    """Structure definition of foaf:Agent"""

    portal_type = CT_FOAF_AGENT


@implementer(IStructure)
@adapter(ISKOSConceptScheme)
class StructSKOSConceptScheme(StructBase):
    """Structure definition of skos:ConceptSchema"""

    portal_type = CT_SKOS_CONCEPTSCHEME


@implementer(IStructure)
@adapter(ISKOSConcept)
class StructSKOSConcept(StructBase):
    """Structure definition of skos:Concept"""

    portal_type = CT_SKOS_CONCEPT
