# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
import zope.schema as schema
from z3c.form.interfaces import IObjectFactory
from z3c.form.object import FactoryAdapter, getIfName
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.interface import implementer
from pkan.dcatapde import _


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
    portal_type='foafagent'

import plone.api.content
import zope.component
from zope.component.interfaces import IFactory

@implementer(IObjectFactory)
class FoafagentFactory(FactoryAdapter):
    """
    """

    def __call__(self, value):
        factory = queryUtility(IFactory, name='foafagent')
        return factory()

name = getIfName(IFoafagent)
zope.component.provideAdapter(FoafagentFactory, name=name)

#from z3c.form.object import registerFactoryAdapter, FactoryAdapter

#registerFactoryAdapter(IFoafagent, FoafagentFactory)

