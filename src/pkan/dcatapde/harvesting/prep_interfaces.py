# -*- coding: utf-8 -*-
"""Preprocessor Interfaces."""

from zope.interface import Interface


class IPreprocessor(Interface):
    """Base Interface for preprocessing data."""

    def preprocess(self, data):
        """Clear data and return it.

        :param data:
        :return:
        """
        return data


class IPotsdam(IPreprocessor):
    """Preprocessor Marker for Potsdam."""
