# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from plone.dexterity.content import Container
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from zope import schema
from zope.interface import implementer


class IDistribution(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Distribution
    """

    add_title = I18NTextLine(
        title=_(u'Translated Title'),
        required=False,
    )

    add_description = I18NText(
        title=_(u'Translated Description'),
        required=False,
    )

    license = schema.URI(
         title=_(u'Access URI'),
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


@implementer(IDistribution)
class Distribution(Container):
    """
    """
