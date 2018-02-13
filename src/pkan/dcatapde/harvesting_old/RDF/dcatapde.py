# -*- coding: utf-8 -*-
"""Harvesting module for DCAT-AP.de data"""
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.data_cleaner.interfaces import IRDF
from pkan.dcatapde.harvesting.RDF.dcat_dataset import RDF2DCATDataset
from pkan.dcatapde.harvesting.RDF.surf_config import SC_DCAT_CATALOG
from pkan.dcatapde.harvesting.RDF.surf_config import SC_DCAT_DATASET
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
        self.context = content.get(UID=self.harvester.base_object)
        if self.context:
            self.search_surf_class = SC_DCAT_DATASET
        else:
            self.context = portal.get()
            self.search_surf_class = SC_DCAT_CATALOG

    def search_start_entities(self):
        """Determine the entities to crawl into"""
        pass

    def crawl(self, rdfstore):
        self.rdfstore = rdfstore
        self.session = self.rdfstore.session
        top_class = self.session.get_class(self.search_surf_class)
        result = top_class.all().full()
        # TOdo generalize
        for rdf_dataset in result:
            factory = RDF2DCATDataset(rdf_dataset, self.context)
            factory.create()
            # Todo: traverse
