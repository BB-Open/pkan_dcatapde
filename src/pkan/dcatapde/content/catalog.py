# -*- coding: utf-8 -*-
from pkan.dcatapde.content.literal import ILiteral
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
import zope.schema as schema
from zope.interface import implementer
from pkan.dcatapde import _

from foafagent import IFoafagent

class ICatalog(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Catalog
    """

    dct_title = schema.List(
         title=_(u'Title'),
         required=True,
         value_type = schema.Object(ILiteral)
    )

    dct_description = schema.List(
         title=_(u'Description'),
         required=True,
         value_type = schema.Object(ILiteral)
    )

    publisher = schema.Object(
        title=_(u'Publisher'),
        required=True,
        schema=IFoafagent
    )

    license = schema.URI(
         title=_(u'License'),
         required=True
    )

    homepage = schema.URI(
        title=(u'Homepage'),
        required=False
    )

    language = schema.Text(
        title=(u'Sprache'),
        required=False
    )

    issued = schema.Date(
        title=(u'Issued'),
        required=False
    )

    modified = schema.Date(
        title=(u'Modified'),
        required=False
    )


@implementer(ICatalog)
class Catalog(object):
    """
    """
