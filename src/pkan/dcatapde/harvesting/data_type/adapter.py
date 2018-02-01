# -*- coding: utf-8 -*-
"""Preprocessor Adapter."""

from pkan.dcatapde import constants as c
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.data_type.interfaces import IPotsdam
from zope.component import adapter
from zope.interface import implementer


@adapter(IHarvester)
@implementer(IPotsdam)
class Potsdam(object):
    """Potsdam Preprocessor."""

    def __init__(self, obj):
        self.obj = obj

    def clean_data(self, data):

        if c.CT_DCAT_DATASET in data:
            data = self.clean_dataset(data)

        if c.CT_DCAT_DISTRIBUTION in data:
            data = self.clean_distribution(data)

        return data

    def clean_dataset(self, data):
        for x in range(0, len(data[c.CT_DCAT_DATASET])):
            data[c.CT_DCAT_DATASET][x]['title'] = 'Dataset {x}'.format(x=x)

        return data

    def clean_distribution(self, data):
        for x in range(0, len(data[c.CT_DCAT_DISTRIBUTION])):
            title = 'Distribution {x}'.format(
                x=x,
            )
            data[c.CT_DCAT_DISTRIBUTION][x]['title'] = title
        return data
