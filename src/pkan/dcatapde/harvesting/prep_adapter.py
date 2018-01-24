# -*- coding: utf-8 -*-
from pkan.dcatapde import constants as c
from pkan.dcatapde.harvesting.interfaces import IImportSource
from pkan.dcatapde.harvesting.prep_interfaces import IPotsdam
from zope.component import adapter
from zope.interface import implementer


@adapter(IImportSource)
@implementer(IPotsdam)
class PotsdamPreprocessor(object):

    def __init__(self, obj):
        self.obj = obj

    def preprocess(self, data):

        for x in range(0, len(data[c.CT_Dataset])):
            data[c.CT_Dataset][x]['title'] = 'Dataset {x}'.format(x=x)

        for x in range(0, len(data[c.CT_Distribution])):
            data[c.CT_Distribution][x]['title'] = 'Distribution {x}'.format(
                x=x
            )

        return data
