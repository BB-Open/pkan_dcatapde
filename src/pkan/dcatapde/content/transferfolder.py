# -*- coding: utf-8 -*-
""""Transfer Folder Content Type."""

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class ITransferfolder(model.Schema):
    """Marker interface and Dexterity Python Schema for Transferfolder."""


@implementer(ITransferfolder)
class Transferfolder(Container):
    """Transfer Folder Content Type."""
