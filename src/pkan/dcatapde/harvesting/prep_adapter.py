# -*- coding: utf-8 -*-
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
        return data
