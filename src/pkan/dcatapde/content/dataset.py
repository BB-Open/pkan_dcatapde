# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.api.dataset import add_dataset
from pkan.dcatapde.constants import CT_Dataset
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.formwidget.relateditems import RelatedItemsFieldWidget
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from z3c.relationfield import RelationChoice
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

    uri = schema.URI(
        title=_(u'URI'),
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


@implementer(IDataset)
class Dataset(Container):
    """
    """


class DatasetDefaultFactory(DexterityFactory):

    def __init__(self):
        self.portal_type = CT_Dataset

    def __call__(self, *args, **kw):
        # TODO: get context and maybe change it
        data = add_dataset(None, dry_run=True, **kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
