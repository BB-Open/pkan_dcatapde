# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer

import zope.schema as schema


class IFoafagent(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Foafagent
    """

    name = schema.TextLine(
         title=_(u'Name'),
         required=True
    )


@implementer(IFoafagent)
class Foafagent(Item):
    """
    """
