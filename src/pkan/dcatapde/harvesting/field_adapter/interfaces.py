# -*- coding: utf-8 -*-
from zope.interface import Interface


class IFieldProcessor(Interface):

    def get_terms_for_vocab(self, ct, field_name):
        pass

    def clean_value(self):
        pass
