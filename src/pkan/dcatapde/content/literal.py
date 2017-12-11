# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from pkan.dcatapde import _


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
