# -*- coding: utf-8 -*-
"""Data Type Interfaces."""

from zope.interface import Interface


class IDataType(Interface):
    """Base Interface for preprocessing data."""

    def clean_data(self, data_storage):
        """Clean data.

        :param data_storage:
        DataStorage-Instance for managing the data

        :return:
        """
        return


class IPotsdamCleaner(IDataType):
    """Marker for Potsdam."""
