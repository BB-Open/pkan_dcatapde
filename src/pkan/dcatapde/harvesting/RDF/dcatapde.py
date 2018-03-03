# -*- coding: utf-8 -*-
"""Harvesting module for DCAT-AP.de data"""
from pkan.dcatapde.content.harvester import IHarvester
# from pkan.dcatapde.harvesting.RDF.dcat_dataset import RDF2DCATDataset
from pkan.dcatapde.harvesting.RDF.interfaces import IRDF
from pkan.dcatapde.harvesting.RDF.surf_config import SC_DCAT_CATALOG
from pkan.dcatapde.harvesting.RDF.surf_config import SC_DCAT_DATASET
from pkan.dcatapde.structure.sparql import QUERY_A
from pkan.dcatapde.structure.structure import (
    StructDCATCatalog,
    StructDCATDataset, )
from plone.api import content
from plone.api import portal
from zope.component import adapter
from zope.interface import implementer


@adapter(IHarvester)
@implementer(IRDF)
class RDFCrawler(object):
    """Crawls a RDF graph stating a a certain baselevel given by the
    datatype of the context. E.G. if the context is a catalog the crawler
    per default searches for datasets in the graph a attaches them to the
    context.
    Alternatively an entity type can be specified to determine the graph
    start points. This is handy if e.g. catalogs are nested into each other."""

    def __init__(self, harvester, search_surf_class=None):
        self.harvester = harvester
        # check if we get a base object
        if self.harvester.base_object:
            self.context = content.get(UID=self.harvester.base_object)
            self.struct_class = StructDCATDataset
        else:
            self.context = portal.get()
            self.struct_class = StructDCATCatalog

    def search_start_entities(self):
        """Determine the entities to crawl into"""
        pass

    def crawl(self):
        top_struct = self.struct_class(self.harvester)
        if top_struct.rdf_type in self.harvester.mapper:
            query = self.harvester.mapper[top_struct.rdf_type]
        else:
            query = QUERY_A.format(top_struct.rdf_type)

        res = self.harvester.graph.query(query)
        pass
