# -*- coding: utf-8 -*-
from zope.interface import Attribute
from zope.interface import Interface


class IHarvestingType(Interface):

    cts = Attribute(
        'Ordered Dictionary mapping ct to parent or None',
    )

    def get_pass_cts(self, context):
        """
        :param context:
        :return: a list of cts, which can be ignored related to context
        """


class IDefaultType(IHarvestingType):
    """Marker Interface for Default"""


class ILicenseType(IHarvestingType):
    """Marker for License Import"""
