# -*- coding: utf-8 -*-
from pkan.dcatapde.content.literal import ILiteral
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer, alsoProvides
from pkan.dcatapde import _


class IDistribution(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Distribution
    """

    add_title = schema.List(
         title=_(u'Translated Title'),
         required=False,
         value_type = schema.Object(ILiteral),
    )

    add_description = schema.List(
         title=_(u'Translated Description'),
         required=False,
         value_type = schema.Object(ILiteral)
    )

    license = schema.URI(
         title=_(u'Access URI'),
         required=True
    )

    license = schema.URI(
         title=_(u'License'),
         required=True
    )

    dct_issued = schema.Date(
        title=(u'Issued'),
        required=False
    )

    dct_modified = schema.Date(
        title=(u'Modified'),
        required=False
    )

alsoProvides(ILiteral)

@implementer(IDistribution)
class Distribution(Container):
    """
    """
