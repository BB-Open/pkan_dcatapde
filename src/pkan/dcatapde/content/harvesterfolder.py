# -*- coding: utf-8 -*-
""""Harvester Folder Content Type."""

from pkan.dcatapde.constants import CT_HARVESTER_FOLDER
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from zope.interface import implementer


class IHarvesterfolder(model.Schema):
    """Marker interface and Dexterity Python Schema for Harvesterfolder."""


@implementer(IHarvesterfolder)
class Harvesterfolder(Container):
    """Harvester Folder Content Type."""


class HarvesterFolderDefaultFactory(DexterityFactory):
    """Custom DX factory for Harvester Folder."""

    def __init__(self):
        self.portal_type = CT_HARVESTER_FOLDER

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.harvester import clean_harvesterfolder
        data, errors = clean_harvesterfolder(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
