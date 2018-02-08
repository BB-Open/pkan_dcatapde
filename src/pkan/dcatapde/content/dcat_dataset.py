# -*- coding: utf-8 -*-
"""DCATDataset Content Type."""

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from pkan.widgets.ajaxselect import AjaxSelectAddFieldWidget
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope.interface import implementer

import zope.schema as schema


class IDCATDataset(model.Schema):
    """Marker interface and Dexterity Python Schema for DCATDataset."""

    # Fieldsets
    # -------------------------------------------------------------------------
    model.fieldset(
        'agents',
        label=i18n.FIELDSET_AGENTS,
        fields=[
            'dct_publisher',
            'dct_creator',
            'dct_contributor',
            'dcatde_originator',
            'dcatde_maintainer',
        ],
    )

    model.fieldset(
        'details',
        label=i18n.FIELDSET_DETAILS,
        fields=[
            'dct_issued',
            'dct_modified',
            'dcatde_politicalGeocodingURI',
            'dcatde_politicalGeocodingLevelURI',
            'dct_identifier',
            'owl_versionInfo',
            'dcatde_legalbasisText',
            'adms_versionNotes',
            'foaf_landingpage',
            'foaf_page',

        ],
    )

    # Mandatory
    # -------------------------------------------------------------------------
    dct_title = I18NTextLine(
        required=True,
        title=i18n.LABEL_DCT_TITLE,
    )

    dct_description = I18NText(
        required=True,
        title=i18n.LABEL_DCT_DESCRIPTION,
    )

    dcatde_contributorID = I18NTextLine(
        required=True,
        title=i18n.LABEL_DCATDE_CONTRIBUTORID,
    )

    rdf_about = schema.URI(
        required=True,
        title=i18n.LABEL_RDF_ABOUT,
    )

    form.widget(
        'dct_publisher',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_FOAF_AGENT,
        content_type_title=i18n.LABEL_DCT_PUBLISHER,
        initial_path='/publisher/',
    )
    dct_publisher = schema.Choice(
        description=i18n.HELP_DCT_PUBLISHER,
        required=True,
        title=i18n.LABEL_DCT_PUBLISHER,
        vocabulary='pkan.dcatapde.vocabularies.FOAFAgent',
    )

    # Recommended
    # -------------------------------------------------------------------------
    form.widget(
        'dct_creator',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_FOAF_AGENT,
        content_type_title=i18n.LABEL_DCT_CREATOR,
        initial_path='/agents/',
    )
    dct_creator = schema.Choice(
        description=i18n.HELP_DCT_CREATOR,
        required=False,
        title=i18n.LABEL_DCT_CREATOR,
        vocabulary='pkan.dcatapde.vocabularies.FOAFAgent',
    )

    form.widget(
        'dct_contributor',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_FOAF_AGENT,
        content_type_title=i18n.LABEL_DCT_CONTRIBUTOR,
        initial_path='/agents/',
    )
    dct_contributor = schema.Choice(
        description=i18n.HELP_DCT_CONTRIBUTOR,
        required=False,
        title=i18n.LABEL_DCT_CONTRIBUTOR,
        vocabulary='pkan.dcatapde.vocabularies.FOAFAgent',
    )

    form.widget(
        'dcatde_originator',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_FOAF_AGENT,
        content_type_title=i18n.LABEL_DCATDE_ORIGINATOR,
        initial_path='/agents/',
    )
    dcatde_originator = schema.Choice(
        description=i18n.HELP_DACTDE_ORIGINATOR,
        required=False,
        title=i18n.LABEL_DCATDE_ORIGINATOR,
        vocabulary='pkan.dcatapde.vocabularies.FOAFAgent',
    )

    form.widget(
        'dcatde_maintainer',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_FOAF_AGENT,
        content_type_title=i18n.LABEL_DCATDE_MAINTAINER,
        initial_path='/agents/',
    )
    dcatde_maintainer = schema.Choice(
        description=i18n.HELP_DACTDE_MAINTAINER,
        required=False,
        title=i18n.LABEL_DCATDE_MAINTAINER,
        vocabulary='pkan.dcatapde.vocabularies.FOAFAgent',
    )

    dct_issued = schema.Date(
        required=False,
        title=i18n.LABEL_DCT_ISSUED,
    )

    dct_modified = schema.Date(
        required=False,
        title=i18n.LABEL_DCT_MODIFIED,
    )

    dcatde_geocodingText = I18NTextLine(
        required=False,
        title=i18n.LABEL_DCATDE_GEOCODINGTEXT,
    )

    dcatde_politicalGeocodingURI = schema.URI(
        required=False,
        title=i18n.LABEL_DCATDE_POLITICALGEOCODINGURI,
    )

    dcatde_politicalGeocodingLevelURI = schema.URI(
        required=False,
        title=i18n.LABEL_DCATDE_POLITICALGEOCODINGLEVELURI,
    )

    dct_identifier = I18NTextLine(
        required=False,
        title=i18n.LABEL_DCT_IDENTIFIER,
    )

    owl_versionInfo = I18NTextLine(
        required=False,
        title=i18n.LABEL_OWL_VERSIONINFO,
    )

    dcatde_legalbasisText = I18NTextLine(
        required=False,
        title=i18n.LABEL_DCATDE_LEGALBASISTEXT,
    )

    adms_versionNotes = I18NTextLine(
        required=False,
        title=i18n.LABEL_ADMS_VERSIONNOTES,
    )

    foaf_landingpage = schema.URI(
        required=False,
        title=i18n.LABEL_FOAF_LANDINGPAGE,
    )

    foaf_page = schema.URI(
        required=False,
        title=i18n.LABEL_FOAF_PAGE,
    )


@implementer(IDCATDataset)
class DCATDataset(Container, DCATMixin):
    """DCATDataset Content Type."""

    _namespace = 'dcat'
    _ns_class = 'dataset'

    dct_title = I18NTextProperty(IDCATDataset['dct_title'])
    dct_description = I18NTextProperty(IDCATDataset['dct_description'])
    dcatde_contributorID = I18NTextProperty(
        IDCATDataset['dcatde_contributorID'],
    )
    dcatde_geocodingText = I18NTextProperty(
        IDCATDataset['dcatde_geocodingText'],
    )
    dct_identifier = I18NTextProperty(IDCATDataset['dct_identifier'])
    owl_versionInfo = I18NTextProperty(IDCATDataset['owl_versionInfo'])
    dcatde_legalbasisText = I18NTextProperty(
        IDCATDataset['dcatde_legalbasisText'],
    )
    adms_versionNotes = I18NTextProperty(IDCATDataset['adms_versionNotes'])

    def Title(self):
        return unicode(self.dct_title)

    def Description(self):
        return unicode(self.dct_description)


class DCATDatasetDefaultFactory(DexterityFactory):
    """Custom DX factory for DCATDataset."""

    def __init__(self):
        self.portal_type = constants.CT_DCAT_DATASET

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.dataset import clean_dataset
        data, errors = clean_dataset(**kw)

        return super(
            DCATDatasetDefaultFactory,
            self,
        ).__call__(*args, **data)
