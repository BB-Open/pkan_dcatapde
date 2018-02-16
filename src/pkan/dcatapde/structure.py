# -*- coding: utf-8 -*-
"""Structure of the dcat-AP.de scheme"""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.constants import CT_DCAT_DISTRIBUTION
from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.constants import CT_DCT_LOCATION
from pkan.dcatapde.constants import CT_FOAF_AGENT
from pkan.dcatapde.constants import CT_RDF_LITERAL
from pkan.dcatapde.marshall.source.dx2any import get_ordered_fields
from plone.api import portal
from plone.api.portal import get_current_language
from zope.i18n import translate
from zope.schema.vocabulary import SimpleTerm


class StructBase(object):
    """Utility functions for all structure classes"""

    # The content type this structure represents
    portal_type = None

    # caching
    _fields_in_order = None
    _fields_objects_required = {}

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


class StructFOAFAgent(StructBase):
    """Structure definition of foaf:Agent"""

    portal_type = CT_FOAF_AGENT

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
