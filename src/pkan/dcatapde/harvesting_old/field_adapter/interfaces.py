# -*- coding: utf-8 -*-
from zope.interface import Interface


class IFieldProcessor(Interface):

    def get_terms_for_vocab(self, ct, field_name, prefix='', required=False):
        pass

    def clean_value(self, data, field_id):
        pass
