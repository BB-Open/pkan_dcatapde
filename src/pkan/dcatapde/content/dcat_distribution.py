# -*- coding: utf-8 -*-
"""DCATDistribution Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DCAT_DISTRIBUTION
from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.content.base import DCATMixin
from pkan.widgets import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from z3c.relationfield import RelationChoice
from zope import schema
from zope.interface import implementer


class IDCATDistribution(model.Schema):
    """Marker interfce and Dexterity Python Schema for DCATDistribution."""

    dct_title = I18NTextLine(
        required=False,
        title=_(u'Title'),
    )

    dct_description = I18NText(
        required=False,
        title=_(u'Description'),
    )

    form.widget(
        'dct_license',
        RelatedItemsFieldWidget,
        content_type=CT_DCT_LICENSEDOCUMENT,
        content_type_title=_(u'License'),
        initial_path='/licenses/',
        pattern_options={
            'selectableTypes': [CT_DCT_LICENSEDOCUMENT],
        },
    )

    dct_license = RelationChoice(
        required=True,
        title=_(u'License'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    dcat_accessURL = schema.URI(
        required=False,
        title=_(u'Access URL'),
    )

    dcat_downloadURL = schema.URI(
        required=False,
        title=_(u'Download URL'),
    )

    dcatde_plannedAvailability = I18NText(
        required=False,
        title=_(u'Planed availability'),
    )

    dcatde_licenseAttributionByText = I18NText(
        required=False,
        title=_(u'Licence attribution by text'),
    )

    dcat_byteSize = I18NText(
        required=False,
        title=_(u'Byte size'),
    )

    form.widget(
        'dct_conformsTo',
        RelatedItemsFieldWidget,
        content_type='dctstandard',
        content_type_title=_(u'Standards'),
        initial_path='/standards/',
        pattern_options={
            'selectableTypes': ['dctstandard'],
        },
    )

    dct_conformsTo = RelationChoice(
        required=False,
        title=_(u'Standards'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(
        'dct_format',
        RelatedItemsFieldWidget,
        content_type='dct_mediatypeorextent',
        content_type_title=_(u'Format'),
        initial_path='/formats/',
        pattern_options={
            'selectableTypes': ['dct_mediatypeorextent'],
        },
    )

    dct_format = RelationChoice(
        required=False,
        title=_(u'Format'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    form.widget(
        'dcat_mediatype',
        RelatedItemsFieldWidget,
        content_type='dct_mediatypeorextent',
        content_type_title=_(u'Media type'),
        initial_path='/formats/',
        pattern_options={
            'selectableTypes': ['dct_mediatypeorextent'],
        },
    )

    dcat_mediatype = RelationChoice(
        required=True,
        title=_(u'Media type'),
        vocabulary='plone.app.vocabularies.Catalog',
    )

    dct_issued = schema.Date(
        required=False,
        title=(u'Issued'),
    )

    dct_modified = schema.Date(
        required=False,
        title=(u'Modified'),
    )


@implementer(IDCATDistribution)
class DCATDistribution(Container, DCATMixin):
    """DCATDistribution Content Type."""

    _namespace = 'dcat'
    _ns_class = 'distribution'


class DCATDistributionDefaultFactory(DexterityFactory):
    """Custom DX factory for DCATDistribution."""

    def __init__(self):
        self.portal_type = CT_DCAT_DISTRIBUTION

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.distribution import clean_distribution
        data, errors = clean_distribution(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
