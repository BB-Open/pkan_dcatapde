# -*- coding: utf-8 -*-
"""Harvester interfaces."""

from zope.interface import Interface


class IImportSource(Interface):
    """Base Interface for Source types."""
    # Todo: new Import requires different fields/methods

    def dry_run(self):
        """Dry Run: Returns Log-Information.
             :return: log information
        """

    def real_run(self):
        """Create Objects.
        :return: log information
        """


class IRDFJSONLD(IImportSource):
    """Interface for JSONLD data."""


class IRDFXML(IImportSource):
    """Interface for RDF/XML data."""


class IRDFTTL(IImportSource):
    """Interface for RDF/Turtle data."""
