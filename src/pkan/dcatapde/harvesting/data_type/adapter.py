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

    def clean_data(self, data_manager):

        if c.CT_DCAT_DATASET in data_manager.data:
            self.clean_dataset(data_manager)

        if c.CT_DCAT_DISTRIBUTION in data_manager.data:
            self.clean_distribution(data_manager)

    def clean_dataset(self, data_manager):
        for id in data_manager.ids:
            title = 'Dataset {x}'.format(
                x=data_manager.ids.index(id),
            ),
            data_manager.reset_attribute(
                c.CT_DCAT_DATASET,
                id,
                'title',
                payload=title,
            )

    def clean_distribution(self, data_manager):
        for id in data_manager.ids:
            title = 'Distribution {x}'.format(
                x=data_manager.ids.index(id),
            )
            data_manager.reset_attribute(
                c.CT_DCAT_DISTRIBUTION,
                id,
                'title',
                payload=title,
            )
