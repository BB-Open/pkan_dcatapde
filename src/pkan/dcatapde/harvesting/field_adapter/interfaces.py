# -*- coding: utf-8 -*-
from zope.interface import Interface


class IFieldProcessor(Interface):

    def get_terms_for_vocab(self, ct, field_name, prefix='', required=False):
        """
        Manages terms for vocab. Returns a list of SimpleTerms.
        Number of Terms depends on Field-Type.
        :param ct:
        :param field_name:
        :param prefix:
        :param required:
        :return:
        """
        pass

    def clean_value(self, data, field_id):
        """
        Clean values.
        Recombind splitted fields. Convert data in correct types.
        :param data:
        :param field_id:
        :return:
        """
        pass
