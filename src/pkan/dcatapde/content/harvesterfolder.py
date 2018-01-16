# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IHarvesterfolder(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Harvesterfolder
    """


@implementer(IHarvesterfolder)
class Harvesterfolder(Container):
    """
    """
    # TODO: create over api
