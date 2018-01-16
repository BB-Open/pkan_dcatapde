# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IHarvesterFieldConfig(model.Schema):
    """ Marker interface and Dexterity Python Schema for HarvesterFieldConfig
    """


@implementer(IHarvesterFieldConfig)
class HarvesterFieldConfig(Container):
    """
    """
