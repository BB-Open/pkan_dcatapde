# -*- coding: utf-8 -*-
"""Plone Harvesting Manager."""

from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.manager.interfaces import IRDFJSONLD
from pkan.dcatapde.harvesting.manager.interfaces import IRDFTTL
from pkan.dcatapde.harvesting.manager.interfaces import IRDFXML
from pkan.dcatapde.harvesting.processors.rdf2plone import PloneRDFProcessor
from pkan.dcatapde.harvesting.processors.visitors import DCATVisitor
from pkan.dcatapde.harvesting.processors.visitors import RealRunVisitor
from zope.component import adapter
from zope.interface import implementer

import datetime


@adapter(IHarvester)
@implementer(IRDFTTL)
@implementer(IRDFJSONLD)
@implementer(IRDFXML)
class TripleStoreHarvestManager(object):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    def __init__(self, harvester, raise_exceptions=True):
        super(TripleStoreHarvestManager, self).__init__(harvester,
                                                        raise_exceptions)
        self.tripel_tempdb = None    # Temporary tripel store
        self.tripeldb = None         # Tripestore for dcapt-ap.de data
        self._target_graph = None        # Target graph instance

    def dry_run(self):
        self.processor = PloneRDFProcessor(self.harvester)
        visitor = DCATVisitor()
        return self.processor.prepare_and_run(visitor)

    def real_run(self):
        self.harvester.last_run = datetime.datetime.now()
        self.processor = PloneRDFProcessor(self.harvester)
        visitor = RealRunVisitor()
        return self.processor.prepare_and_run(visitor)
