# -*- coding: utf-8 -*-
from plone.dexterity.factory import DexterityFactory

from pkan.dcatapde import _
from plone.dexterity.content import Container
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from zope import schema
from zope.interface import implementer

from pkan.dcatapde.api.distribution import add_distribution
from pkan.dcatapde.constants import CT_Distribution


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


class DistributionDefaultFactory(DexterityFactory):

    def __init__(self):
        self.portal_type = CT_Distribution

    def __call__(self, *args, **kw):
        # TODO: get context and maybe change it
        data = add_distribution(None, dry_run=True, **kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
