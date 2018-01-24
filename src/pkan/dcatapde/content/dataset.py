# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.api.dataset import add_dataset
from pkan.dcatapde.constants import CT_Dataset
from pkan.dcatapde.content.catalog import INameFromCatalog
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

    dct_title = I18NTextLine(
        title=_(u'Title'),
        required=True,
    )

    dct_description = I18NText(
        title=_(u'Description'),
        required=True,
    )

    dcatde_contributorID = I18NTextLine(
        title=_(u'Title'),
        required=True,
    )

    dct_license = schema.URI(
         title=_(u'License'),
         required=True
    )

    uri = schema.URI(
        title=_(u'URI'),
        required=True
    )

    form.widget(
        'dcatde_contributor',
        RelatedItemsFieldWidget,
        content_type='foafagent',
        content_type_title=_(u'Contributor'),
        initial_path='/',
        pattern_options={
            'selectableTypes': ['foafagent'],
        }
    )

    dcatde_contributor = RelationChoice(
        title=_(u'Contributor'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )


    dct_issued = schema.Date(
        title=(u'Issued'),
        required=False
    )

    dct_modified = schema.Date(
        title=(u'Modified'),
        required=False
    )

    dcatde_politicalGeocodingURI =schema.URI(
         title=_(u'PoliticalGeocodingURI'),
         required=False
    )

    dcatde_politicalGeocodingLevelURI = schema.URI(
         title=_(u'PoliticalGeocodingLevelURI'),
         required=False
    )

    dct_identifier = I18NTextLine(
        title=_(u'Identifier'),
        required=False,
    )

    owl_versionInfo = I18NTextLine(
        title=_(u'Version info'),
        required=False,
    )
    dcatde_legalbasisText  = I18NTextLine(
        title=_(u'Legal basis text'),
        required=False,
    )
    adms_versionNotes = I18NTextLine(
        title=_(u'Version Notes'),
        required=False,
    )

@implementer(IDataset)
class Dataset(Container):
    """
    """
    _Title = ''

    def Title(self):
        if not self._Title:
            self._Title = INameFromCatalog(self).title
        return self._Title




class DatasetDefaultFactory(DexterityFactory):

    def __init__(self):
        self.portal_type = CT_Dataset

    def __call__(self, *args, **kw):
        # TODO: get context and maybe change it
        data = add_dataset(None, dry_run=True, **kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
