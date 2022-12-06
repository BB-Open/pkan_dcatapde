# -*- coding: utf-8 -*-
"""Harvesting Errors"""


class RequiredPredicateMissing(Exception):
    """RequiredPredicateMissing"""


class UnkownBindingType(Exception):
    """UnkownBindingType"""


class NoSourcesDefined(Exception):
    """No Urls to load RDF for harvest"""

class GeoHarvestingFailed(Exception):
    """Failed Geo Harvesting"""
