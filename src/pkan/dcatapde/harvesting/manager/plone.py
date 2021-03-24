# -*- coding: utf-8 -*-
"""Plone Harvesting Manager."""

from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.constants import RDF_FORMAT_METADATA
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.manager.base import IFaceToRDFFormatKey
from pkan.dcatapde.harvesting.manager.interfaces import IRDFJSONLD
from pkan.dcatapde.harvesting.manager.interfaces import IRDFTTL
from pkan.dcatapde.harvesting.manager.interfaces import IRDFXML
from pkan.dcatapde.harvesting.processors.rdf2plone import PloneRDFProcessor
from pkan.dcatapde.harvesting.processors.visitors import DCATVisitor
from pkan.dcatapde.harvesting.processors.visitors import RealRunVisitor
from pkan.dcatapde.structure.structure import StructDCATCatalog
from pkan.dcatapde.structure.structure import StructDCATDataset
from pkan.dcatapde.utils import get_default_language
from pkan.dcatapde.utils import LiteralHandler
from plone.api import content
from zope.component import adapter
from zope.interface import implementer

import datetime


@adapter(IHarvester)
@implementer(IRDFTTL)
@implementer(IRDFJSONLD)
@implementer(IRDFXML)
class PloneHarvestManager(object):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    def __init__(self, harvester, raise_exceptions=False):
        # remember the harvester
        self.harvester = harvester
        self.raise_exceptions = raise_exceptions
        # look if we have a harvesting type adapter
        # try:
        #     self.harvesting_type = \
        #         self.harvester.harvesting_type(self.harvester)
        # except TypeError:
        #     self.harvesting_type = None

        # fetch the preprocessor adapter
        # self.data_cleaner = self.harvester.data_cleaner(self.harvester)
        self.cleaned_data = None
        # self.field_config = get_field_config(self.harvester)
        self.harvesting_context = self.harvester
        if self.harvester:
            if getattr(self.harvester, 'base_object', None):
                self.harvesting_context = content.get(
                    UID=self.harvester.base_object,
                )

        # check which top_node we should use
        if getattr(self.harvester, 'top_node', None) and \
                self.harvester.top_node == CT_DCAT_DATASET:
            self.struct_class = StructDCATDataset
        elif self.harvester.top_node == CT_DCAT_CATALOG:
            self.struct_class = StructDCATCatalog
        else:
            self.struct_class = None

        # determine the source format serializer string for rdflib from our
        # own interface. Todo this is a bit ugly
        self.rdf_format_key = IFaceToRDFFormatKey[self.harvester.source_type]
        self.rdf_format = RDF_FORMAT_METADATA[self.rdf_format_key]
        self.serialize_format = self.rdf_format['serialize_as']
        self.mime_type = self.rdf_format['mime_type']
        self.def_lang = get_default_language()
        self.literal_handler = LiteralHandler()
        self.setup_logger()
        self.get_entity_mapping()

    def dry_run(self):
        self.processor = PloneRDFProcessor(self.harvester)
        visitor = DCATVisitor()
        return self.processor.prepare_and_run(visitor)

    def real_run(self):
        self.harvester.last_run = datetime.datetime.now()
        self.processor = PloneRDFProcessor(self.harvester)
        visitor = RealRunVisitor()
        return self.processor.prepare_and_run(visitor)
