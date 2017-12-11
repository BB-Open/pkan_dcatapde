# -*- coding: utf-8 -*-
from pkan.dcatapde.content.literal import ILiteral
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
import zope.schema as schema
from zope.interface import implementer
from pkan.dcatapde import _


class IDataset(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Dataset
    """

    title = schema.Object(
         title=_(u'Title'),
         required=True,
         schema=ILiteral
    )

    description = schema.Object(
         title=_(u'Description'),
         required=True,
         schema=ILiteral
    )

    contributorID = schema.List(
         title=_(u'Contributor'),
         required=True,
         value_type = schema.Object(ILiteral)
    )

@implementer(IDataset)
class Dataset(Container):
    """
    """
