# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.form.interfaces import IObjectFactory
from z3c.form.object import FactoryAdapter
from z3c.form.object import getIfName
from zope.component import queryUtility
from zope.component.interfaces import IFactory
from zope.interface import implementer

import zope.component
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
    portal_type = 'foafagent'


@implementer(IObjectFactory)
class FoafagentFactory(FactoryAdapter):
    """
    """

    def __call__(self, value):
        factory = queryUtility(IFactory, name='foafagent')
        return factory()


name = getIfName(IFoafagent)
zope.component.provideAdapter(FoafagentFactory, name=name)
