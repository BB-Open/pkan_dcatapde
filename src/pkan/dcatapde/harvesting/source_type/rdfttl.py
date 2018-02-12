# -*- coding: utf-8 -*-
"""Harvesting adapter."""
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.source_type.interfaces import IRDFTTL
from zope.component import adapter
from zope.interface import implementer


@adapter(IHarvester)
@implementer(IRDFTTL)
class XmlProcessor(object):
    """RDF/TTL Processor."""

    def dry_run(self):
        """Dry Run: Returns Log-Information.
        """
