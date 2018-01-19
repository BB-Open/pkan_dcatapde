# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from zope.interface import implementer

from pkan.dcatapde.api.harvester import add_harvester_folder
from pkan.dcatapde.constants import CT_HarvesterFolder


class IHarvesterfolder(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Harvesterfolder
    """


@implementer(IHarvesterfolder)
class Harvesterfolder(Container):
    """
    """



class HarvesterFolderDefaultFactory(DexterityFactory):

    def __init__(self):
        self.portal_type = CT_HarvesterFolder

    def __call__(self, *args, **kw):
        # TODO: get context and maybe change it
        data = add_harvester_folder(None, dry_run=True, **kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder