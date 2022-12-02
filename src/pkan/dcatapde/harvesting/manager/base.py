# -*- coding: utf-8 -*-
"""Harvesting manager."""
import datetime

from pkan.dcatapde.harvesting.load_data.rdf_base import BaseRDFProcessor
from pkan.dcatapde.harvesting.load_data.visitors import DCATVisitor
from pkan.dcatapde.harvesting.load_data.visitors import RealRunVisitor
from zope.component import adapter
from zope.interface import implementer

from pkan.dcatapde.constants import RDF_FORMAT_JSONLD
from pkan.dcatapde.constants import RDF_FORMAT_TURTLE
from pkan.dcatapde.constants import RDF_FORMAT_XML
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.manager.interfaces import IRDFJSONLD
from pkan.dcatapde.harvesting.manager.interfaces import IRDFTTL
from pkan.dcatapde.harvesting.manager.interfaces import IRDFXML

IFaceToRDFFormatKey = {
    IRDFTTL: RDF_FORMAT_TURTLE,
    IRDFJSONLD: RDF_FORMAT_JSONLD,
    IRDFXML: RDF_FORMAT_XML,
}


@adapter(IHarvester)
@implementer(IRDFTTL)
@implementer(IRDFJSONLD)
@implementer(IRDFXML)
class BaseHarvestManager(object):
    """Manages the harvest from the plone side"""

    def __init__(self, harvester, raise_exceptions=False):
        # remember the harvester
        self.harvester = harvester
        self.raise_exceptions = raise_exceptions

    def dry_run(self):
        self.processor = BaseRDFProcessor(self)
        visitor = DCATVisitor()
        return self.processor.prepare_and_run(visitor)

    def real_run(self):
        self.harvester.last_run = datetime.datetime.now()
        self.processor = BaseRDFProcessor(self)
        visitor = RealRunVisitor()
        return self.processor.prepare_and_run(visitor)
