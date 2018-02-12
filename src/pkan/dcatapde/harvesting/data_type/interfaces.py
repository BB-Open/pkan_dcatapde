# -*- coding: utf-8 -*-
"""Data Type Interfaces."""

from zope.interface import Interface


class IDataType(Interface):
    """Base Interface for preprocessing data."""

    def clean_data(self, data):
        """Clear data and return it.

        :param data:

        data must be dictionary like

        {ct_identifier: {index: {field: list of data}}}

        :return:
        """
        return data


class INone(IDataType):
    """Preprocessor Marker for Null Processor."""


class IPotsdam(IDataType):
    """Preprocessor Marker for Potsdam."""
