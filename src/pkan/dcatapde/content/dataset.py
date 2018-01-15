# -*- coding: utf-8 -*-

from pkan.dcatapde import _
from pkan.dcatapde.content.foafagent import IFoafagent
from pkan.dcatapde.content.literal import ILiteral
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.formwidget.relateditems import RelatedItemsFieldWidget
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from z3c.form.object import registerFactoryAdapter
from z3c.relationfield import RelationChoice
from zope.interface import alsoProvides
from zope.interface import implementer

import zope.schema as schema


class IDataset(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Dataset
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
        'contributorID',
        RelatedItemsFieldWidget,
        content_type='foafagent',
        content_type_title=_(u'Contributor'),
        initial_path='/',
        pattern_options={
            'selectableTypes': ['foafagent'],
        }
    )
    contributorID = RelationChoice(
        title=_(u'Contributor'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=True,
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


registerFactoryAdapter(IDataset, Dataset)
