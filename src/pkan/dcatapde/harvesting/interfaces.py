# -*- coding: utf-8 -*-
"""Harvester interfaces."""

from zope.interface import Interface


class IImportSource(Interface):
    """Base Interface for Source types."""

    def read_available_fields(self):
        """Read fields from data source.

        :return:
        """

    def read_values(self):
        """Read fields and

        :return:
        """

    def dry_run(self):
        """Dry Run: Returns Log-Information.

        :return:
        """

    def real_run(self):
        """Create Objects.

        :return:
        """


class IJson(IImportSource):
    """Interface for JSON data."""


class IXml(IImportSource):
    """Interface for XML data."""
