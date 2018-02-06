# -*- coding: utf-8 -*-
"""Harvester interfaces."""

from zope.interface import Interface


class IImportSource(Interface):
    """Base Interface for Source types."""

    def read_available_fields(self):
        """Read fields from data source.

        :return: list of fields
        """

    def read_dcat_fields(self, ct=None):
        """
        Read fields for dcat plone objects
        :return: Terms for vocabulary
        """

    def read_values(self):
        """Read field values from source url
        Result must be data dict like
        {ct_identifier: {index: {field: list of data}}}

        :return:
        """

    def clean_data(self):
        """
        Clean data in multiple steps:
         1. Field level cleaning
         2. data_type cleaning
         3. data config cleaning
         4. finding duplicates
        Result must be data-dict like
        {ct_identifier: {index: {field: list of data}}}
        :return:
        """

    def dry_run(self):
        """Dry Run: Returns Log-Information.

        :return: log information
        """

    def real_run(self):
        """Create Objects.

        :return: log information
        """


class IJson(IImportSource):
    """Interface for JSON data."""


# class IXml(IImportSource):
#     """Interface for XML data."""
