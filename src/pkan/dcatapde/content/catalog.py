# -*- coding: utf-8 -*-
from foafagent import IFoafagent
from pkan.dcatapde import _
from pkan.dcatapde.content.literal import ILiteral
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.formwidget.relateditems import RelatedItemsFieldWidget
from plone.namedfile import field as namedfile
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from z3c.relationfield import RelationChoice
from zope.interface import alsoProvides
from zope.interface import implementer

import zope.schema as schema


class ICatalog(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Catalog
    """

    add_title = I18NTextLine(
        title=_(u'Translated Title'),
        required=False,
    )

    add_description = I18NText(
        title=_(u'Translated Description'),
        required=False,
    )

    form.widget(
        'publisher',
        RelatedItemsFieldWidget,
        content_type='foafagent',
        content_type_title=_(u'Publisher'),
        initial_path='/',
        pattern_options={
            'selectableTypes': ['foafagent'],
        }
    )
    publisher = RelationChoice(
        title=_(u'Publisher'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=True,
    )

    license = schema.URI(
        title=_(u'License'),
        required=True
    )

    homepage = schema.URI(
        title=(u'Homepage'),
        required=False
    )

    dct_issued = schema.Date(
        title=(u'Issued'),
        required=False
    )

    dct_modified = schema.Date(
        title=(u'Modified'),
        required=False
    )



@implementer(ICatalog)
class Catalog(Container):
    """
    """
