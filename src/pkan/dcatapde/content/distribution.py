# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_Distribution
from pkan.dcatapde.content.catalog import INameFromCatalog
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from z3c.relationfield import RelationChoice
from zope import schema
from zope.interface import implementer


class IDistribution(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Distribution
    """

    dct_title = I18NTextLine(
        title=_(u'Title'),
        required=False,
    )

    dct_description = I18NText(
        title=_(u'Description'),
        required=False,
    )

    dct_license = schema.URI(
         title=_(u'Access URI'),
         required=True
    )

    dcatde_plannedAvailability = I18NText(
        title=_(u'Planed availability'),
        required=False,
    )

    dcatde_licenseAttributionByText = I18NText(
        title=_(u'Licence attribution by text'),
        required=False,
    )

    dcat_byteSize = I18NText(
        title=_(u'Byte size'),
        required=False,
    )

    form.widget(
        'dct_conformsTo',
        RelatedItemsFieldWidget,
        content_type='dctstandard',
        content_type_title=_(u'Standards'),
        initial_path='/standards/',
        pattern_options={
            'selectableTypes': ['dctstandard'],
        }
    )

    dct_conformsTo = RelationChoice(
        title=_(u'Standards'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )

    form.widget(
        'dct_format',
        RelatedItemsFieldWidget,
        content_type='dct_mediatypeorextent',
        content_type_title=_(u'Format'),
        initial_path='/formats/',
        pattern_options={
            'selectableTypes': ['dct_mediatypeorextent'],
        }
    )

    dct_format = RelationChoice(
        title=_(u'Format'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )

    form.widget(
        'dcat_mediatype',
        RelatedItemsFieldWidget,
        content_type='dct_mediatypeorextent',
        content_type_title=_(u'Media type'),
        initial_path='/formats/',
        pattern_options={
            'selectableTypes': ['dct_mediatypeorextent'],
        }
    )

    dcat_mediatype = RelationChoice(
        title=_(u'Media type'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=True,
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
    _Title = ''

    def Title(self):
        if not self._Title:
            self._Title = INameFromCatalog(self).title
        return self._Title


class DistributionDefaultFactory(DexterityFactory):

    def __init__(self):
        self.portal_type = CT_Distribution

    def __call__(self, *args, **kw):
        # TODO: get context and maybe change it
        from pkan.dcatapde.api.distribution import clean_distribution
        data, errors = clean_distribution(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
