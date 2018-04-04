# -*- coding: utf-8 -*-
""""Harvester Folder Content Type."""

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IHarvesterfolder(model.Schema):
    """Marker interface and Dexterity Python Schema for Harvesterfolder."""


@implementer(IHarvesterfolder)
class Harvesterfolder(Container):
    """Harvester Folder Content Type."""
