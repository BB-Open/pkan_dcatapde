# -*- coding: utf-8 -*-
"""Literal Content Type"""

from pkan.dcatapde import _
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class ILiteral(model.Schema):
    """Marker interface and Dexterity Python Schema for Literal."""

    text = schema.TextLine(
        required=True,
        title=_(u'Text'),
    )

    language = schema.TextLine(
        required=False,
        title=_(u'Language'),
    )


@implementer(ILiteral)
class Literal(Item):
    """Literal Content Type."""
