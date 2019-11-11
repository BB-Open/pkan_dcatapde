# -*- coding: utf-8 -*-
"""Harvesting Errors"""


class RequiredPredicateMissing(Exception):
    """RequiredPredicateMissing"""


class HarvestURINotReachable(Exception):
    """HarvestURINotReachable"""


class TripelStoreBulkLoadError(Exception):
    """TripelStoreBulkLoadError"""


class TripelStoreCreateNamespaceError(Exception):
    """TripelStoreCreateNamespaceError"""


class UnkownBindingType(Exception):
    """UnkownBindingType"""
