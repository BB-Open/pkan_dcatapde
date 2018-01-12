# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.form.object import registerFactoryAdapter
from zope import schema
from zope.interface import implementer


class ILiteral(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Literal
    """

    text = schema.TextLine(
         title=_(u'Text'),
         required=True
    )

    language = schema.TextLine(
         title=_(u'Language'),
         required=False
    )


@implementer(ILiteral)
class Literal(Item):
    """
    """


registerFactoryAdapter(ILiteral, Literal)
