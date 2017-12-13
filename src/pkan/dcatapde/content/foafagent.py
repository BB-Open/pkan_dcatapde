# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
import zope.schema as schema
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

from z3c.form.object import registerFactoryAdapter
registerFactoryAdapter(IFoafagent, Foafagent)