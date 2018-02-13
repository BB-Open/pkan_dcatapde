# -*- coding: utf-8 -*-
"""Preprocessor Adapter."""
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.data_cleaner.interfaces import IPotsdamCleaner
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces import IRequest


@adapter(IHarvester, IRequest)
@implementer(IPotsdamCleaner)
class PotsdamCleaner(object):
    """
    Adapter for cleaning Potsdam Data.
    Usable to add missing fields or update incomplete/incorrect fields
    """
    # Todo: rewrite for RDF Import

    def __init__(self, harvester):
        self.harvester = harvester

    def clean_data(self, data_manager):
        """
        Update/Add/Delete data related to data source.

        :param data_manager: data holding instance
        :return:
        """
        pass
