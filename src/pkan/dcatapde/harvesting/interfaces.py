# -*- coding: utf-8 -*-
from zope.interface import Interface


class IImportSource(Interface):
    """
    Base Interface for Source types
    """

    def read_available_fields(self):
        """
        Read fields from data source
        :return:
        """

    def read_values(self):
        '''
        Read fields and
        :return:
        '''


class IJson(IImportSource):
    """
    Interface for JSON data
    """


class IXml(IImportSource):
    """
    Interface for XML data
    """
