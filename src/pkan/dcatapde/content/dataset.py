# -*- coding: utf-8 -*-
from pkan.dcatapde.content.foafagent import IFoafagent
from pkan.dcatapde.content.literal import ILiteral
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
import zope.schema as schema
from zope.interface import implementer, alsoProvides
from pkan.dcatapde import _


class IDataset(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Dataset
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

    contributorID = schema.List(
         title=_(u'Contributor'),
         required=True,
         value_type = schema.Object(IFoafagent)
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

alsoProvides(ILiteral, IFoafagent)

@implementer(IDataset)
class Dataset(Container):
    """
    """

from z3c.form.object import registerFactoryAdapter
registerFactoryAdapter(IDataset, Dataset)