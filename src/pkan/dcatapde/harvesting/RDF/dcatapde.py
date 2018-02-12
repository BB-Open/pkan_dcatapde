# -*- coding: utf-8 -*-
"""Harvesting module for DCAT-AP.de data"""
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.data_type.interfaces import IRDF
from pkan.dcatapde.harvesting.RDF.surf_config import SC_DCAT_CATALOG
from zope.component import adapter
from zope.interface import implementer


@adapter(IHarvester)
@implementer(IRDF)
class RDFCrawler(object):
    """Crawls a RDF graph stating a a certain baselevel given by the
    datatype of the context. E.G. if the context is a catalog the crawler
    per default searches for datasets in the graph a attaches them to the
    context.
    Alternatively a entity type can be specified to determine the graph
    start points. This is handy if e.g. catalogs are nested into each other."""

    def __init__(self, context, search_surf_class=None):
        self.context = context
        if search_surf_class:
            self.search_surf_class = search_surf_class
        else:
            try:
                self.search_surf_class = self.context.surf_class
            except AttributeError:
                # The context is no entity so asume we search for catalogs
                self.search_surf_class = SC_DCAT_CATALOG

    def search_start_entities(self):
        """Determine the entities to crawl into"""
        pass

    def crawl(self, context, entity):
        pass
