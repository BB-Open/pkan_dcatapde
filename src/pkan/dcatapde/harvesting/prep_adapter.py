# -*- coding: utf-8 -*-
"""Preprocessor Adapter."""

from pkan.dcatapde import constants as c
from pkan.dcatapde.harvesting.interfaces import IImportSource
from pkan.dcatapde.harvesting.prep_interfaces import IPotsdam
from zope.component import adapter
from zope.interface import implementer


@adapter(IImportSource)
@implementer(IPotsdam)
class PotsdamPreprocessor(object):
    """Potsdam Preprocessor."""

    def __init__(self, obj):
        self.obj = obj

    def preprocess(self, data):

        if c.CT_Dataset in data:
            data = self.preprocess_dataset(data)

        if c.CT_Distribution in data:
            data = self.preprocess_distribution(data)

        return data

    def preprocess_dataset(self, data):
        for x in range(0, len(data[c.CT_Dataset])):
            data[c.CT_Dataset][x]['title'] = 'Dataset {x}'.format(x=x)

        return data

    def preprocess_distribution(self, data):
        for x in range(0, len(data[c.CT_Distribution])):
            data[c.CT_Distribution][x]['title'] = 'Distribution {x}'.format(
                x=x,
            )
        return data
