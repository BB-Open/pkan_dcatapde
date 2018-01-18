# -*- coding: utf-8 -*-
from pkan.dcatapde.io.marshall.interfaces import IRDFMarshallTarget
from zope.interface import implementer
from zope.interface import Interface


@implementer(IRDFMarshallTarget)
class RDFMarshallTarget(object):

    def __init__(self):
        self.data = {}


    def store_triple(self, s, p, o):
        self.data = {}



