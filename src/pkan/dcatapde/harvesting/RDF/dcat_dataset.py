# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.harvesting.RDF.surf_config import SC_DCAT_DISTRIBUTION
from pkan.dcatapde.harvesting.RDF.surf_config import SC_DCT_LICENSEDOCUMENT
from pkan.dcatapde.harvesting.RDF.surf_config import SC_DCT_LOCATION
from pkan.dcatapde.harvesting.RDF.surf_config import SC_FOAF_AGENT
from pkan.dcatapde.marshall.source.dx2any import get_ordered_fields
from plone.api import content
from plone.api import portal

import rdflib


class RDF2ANY(object):
    """Base factory for RDF2Dexterity"""

    BLACKLIST = [
        'exclude_from_nav',
    ]
    _fields_in_order = None

    def __init__(self, rdf, context):
        self.context = context
        self.rdf = rdf
        self.default_language = portal.get_default_language()
        self.current_language = portal.get_current_language()

    def literal_to_i18n(self, literals):
        if isinstance(literals.first, rdflib.term.Literal):
            att_data = {}
            for literal in literals:
                # check if language attribute exists
                try:
                    att_data[literal.language] = unicode(literal)
                except AttributeError:
                    att_data[self.default_language] = unicode(literal)
        else:
            att_data = unicode(literals.first)

        return att_data

    @property
    def fields_in_order(self):
        if not self._fields_in_order:
            ptypes = portal.get_tool('portal_types')
            fti = ptypes[CT_DCAT_DATASET]
            self._fields_in_order = get_ordered_fields(fti)
        return self._fields_in_order


class RDF2DCATDataset(RDF2ANY):
    """Harvester for DCAT-AP.de Catalogs."""

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
        """Return all contained items.

        :return:
        """
        result = {}
        result['dcat_distribution'] = SC_DCAT_DISTRIBUTION
        return result

    @property
    def referenced(self):
        """Return all referenced items.

        :return:
        """
        related = {}
        related['dct:publisher'] = SC_FOAF_AGENT
        related['dct:license'] = SC_DCT_LICENSEDOCUMENT
        related['dct:spatial'] = SC_DCT_LOCATION
        return related

    def create(self):
        self.data = {}
        for property_name, field in self.properties.items():
            if property_name in self.BLACKLIST:
                continue
            try:
                property_value = getattr(self.rdf, property_name)
            except AttributeError:
                if field.required:
                    raise AttributeError
                continue
            self.data[property_name] = self.literal_to_i18n(property_value)

        for property_name, ns_class in self.referenced.items():
            try:
                property_value = getattr(self.context, property_name)
            except AttributeError:
                # Todo: check for required
                continue
            # test if referenced field is of correct type
            pass

        dct_title = self.data['dct_title']
        if self.default_language in dct_title:
            id = dct_title[self.default_language]
        elif self.current_language in dct_title:
            id = dct_title[self.current_language]
        else:
            id = dct_title[dct_title.keys()[0]]

        # create a dcat_dataset object
        dataset = content.create(
            container=self.context,
            type=CT_DCAT_DATASET,
            id=id,
            **self.data)

        return dataset