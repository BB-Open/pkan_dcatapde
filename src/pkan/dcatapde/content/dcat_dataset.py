# -*- coding: utf-8 -*-
"""DCATDataset Content Type."""
import datetime

import zope.schema as schema
from pkan.widgets.ajaxselect import AjaxSelectAddFieldWidget
from plone.autoform import directives as form
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.dexterity.content import Container
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope.interface import implementer

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.content.base import IDCAT


class IDCATDataset(model.Schema, IDCAT):
    """Marker interface and Dexterity Python Schema for DCATDataset."""

    # Fieldsets
    # -------------------------------------------------------------------------
    model.fieldset(
        'agents',
        label=i18n.FIELDSET_AGENTS,
        fields=[
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
            'dcatde_contributorID',
            'dcatde_politicalGeocodingURI',
            'dcatde_politicalGeocodingLevelURI',
            'dcatde_geocodingText',
            'dct_accessRights',
            'owl_versionInfo',
            'dcatde_legalbasisText',
            'adms_versionNotes',
            'dcat_landingpage',
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

    read_permission(dcatde_contributorID='pkan.dcatapde.ProviderDataEditor')
    write_permission(dcatde_contributorID='pkan.dcatapde.ProviderDataEditor')
    dcatde_contributorID = I18NTextLine(
        required=False,
        title=i18n.LABEL_DCATDE_CONTRIBUTORID,
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
        required=False,
        title=i18n.LABEL_DCT_PUBLISHER,
        vocabulary='pkan.dcatapde.vocabularies.FOAFAgent',
    )

    # Recommended
    # -------------------------------------------------------------------------

    form.widget(
        'dcat_theme',
        AjaxSelectAddFieldWidget,
        display_deprecated=True,
        content_type=constants.CT_SKOS_CONCEPT,
        content_type_title=i18n.LABEL_SKOS_CONCEPT,
        initial_path='/locations/',
    )
    dcat_theme = schema.List(
        description=i18n.HELP_SKOS_CONCEPT,
        required=False,
        title=i18n.LABEL_SKOS_CONCEPT,
        value_type=schema.Choice(
            vocabulary='pkan.dcatapde.vocabularies.SKOSConcept',
        ),
    )

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
        default=datetime.date.today(),
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

    read_permission(owl_versionInfo='pkan.dcatapde.ProviderDataEditor')
    write_permission(owl_versionInfo='pkan.dcatapde.ProviderDataEditor')
    owl_versionInfo = I18NTextLine(
        required=False,
        title=i18n.LABEL_OWL_VERSIONINFO,
    )

    dcatde_legalbasisText = I18NText(
        required=False,
        title=i18n.LABEL_DCATDE_LEGALBASISTEXT,
    )

    form.widget(
        'dct_accessRights',
        AjaxSelectAddFieldWidget,
        display_deprecated=True,
        content_type=constants.CT_DCT_RIGHTSSTATEMENT,
        content_type_title=i18n.LABEL_DCT_ACCESSRIGHTS,
        initial_path='/rights/',
    )
    dct_accessRights = schema.Choice(
        description=i18n.HELP_DCT_ACCESSRIGHTS,
        required=False,
        title=i18n.LABEL_DCT_ACCESSRIGHTS,
        vocabulary='pkan.dcatapde.vocabularies.DCTRightsStatement',
    )

    read_permission(adms_versionNotes='pkan.dcatapde.ProviderDataEditor')
    write_permission(adms_versionNotes='pkan.dcatapde.ProviderDataEditor')
    adms_versionNotes = I18NTextLine(
        required=False,
        title=i18n.LABEL_ADMS_VERSIONNOTES,
    )

    dcat_landingpage = schema.URI(
        required=False,
        title=i18n.LABEL_DCAT_LANDINGPAGE,
    )

    foaf_page = schema.URI(
        required=False,
        title=i18n.LABEL_FOAF_PAGE,
    )

    form.widget(
        'dcat_contactPoint',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_VCARD_KIND,
        content_type_title=i18n.LABEL_VCARD_KIND,
        initial_path='/vcardkinds/',
    )
    dcat_contactPoint = schema.List(
        description=i18n.HELP_VCARD_KIND,
        required=False,
        title=i18n.LABEL_VCARD_KIND,
        value_type=schema.Choice(
            vocabulary='pkan.dcatapde.vocabularies.VCARDKind',
        ),
    )


@implementer(IDCATDataset)
class DCATDataset(Container, DCATMixin):
    """DCATDataset Content Type."""

    portal_type = constants.CT_DCAT_DATASET
    content_schema = IDCATDataset
    _namespace = 'dcat'
    _ns_class = 'Dataset'

    dct_title = I18NTextProperty(IDCATDataset['dct_title'])
    dct_description = I18NTextProperty(IDCATDataset['dct_description'])
    dcatde_contributorID = I18NTextProperty(
        IDCATDataset['dcatde_contributorID'],
    )
    dcatde_geocodingText = I18NTextProperty(
        IDCATDataset['dcatde_geocodingText'],
    )
    owl_versionInfo = I18NTextProperty(IDCATDataset['owl_versionInfo'])
    dcatde_legalbasisText = I18NTextProperty(
        IDCATDataset['dcatde_legalbasisText'],
    )
    adms_versionNotes = I18NTextProperty(IDCATDataset['adms_versionNotes'])

    def Title(self):
        return self.title_from_title_field()

    def Description(self):
        return self.desc_from_desc_field()
