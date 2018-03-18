# -*- coding: utf-8 -*-
"""DCATDistribution Content Type."""

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.content.base import IDCAT
from pkan.widgets.ajaxselect import AjaxSelectAddFieldWidget
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope import schema
from zope.interface import implementer


class IDCATDistribution(model.Schema, IDCAT):
    """Marker interface and Dexterity Python Schema for DCATDistribution."""

    # Mandatory
    # -------------------------------------------------------------------------
    dct_title = I18NTextLine(
        required=False,
        title=i18n.LABEL_DCT_TITLE,
    )

    dct_description = I18NText(
        required=False,
        title=i18n.LABEL_DCT_DESCRIPTION,
    )

    form.widget(
        'dct_license',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_DCT_LICENSEDOCUMENT,
        content_type_title=i18n.LABEL_DCT_LICENSE,
        initial_path='/licenses/',
    )
    dct_license = schema.Choice(
        description=i18n.HELP_DCT_LICENSE,
        required=False,
        title=i18n.LABEL_DCT_LICENSE,
        vocabulary='pkan.dcatapde.vocabularies.DCTLicenseDocument',
    )

    dcat_accessURL = schema.URI(
        required=False,
        title=i18n.LABEL_DCAT_ACCESSURL,
    )

    dcat_downloadURL = schema.URI(
        required=False,
        title=i18n.LABEL_DCAT_DOWNLOADURL,
    )

    dcatde_plannedAvailability = I18NText(
        required=False,
        title=i18n.LABEL_DCATDE_PLANNED_AVAILABLITY,
    )

    dcatde_licenseAttributionByText = I18NText(
        required=False,
        title=i18n.LABEL_DCATDE_LICENSEATTRIBUTIONBYTEXT,
    )

    dcat_byteSize = I18NText(
        required=False,
        title=i18n.LABEL_DCAT_BYTESIZE,
    )

    form.widget(
        'dct_conformsTo',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_DCT_STANDARD,
        content_type_title=i18n.LABEL_DCT_CONFORMSTO,
        initial_path='/standards/',
    )
    dct_conformsTo = schema.Choice(
        description=i18n.HELP_DCT_CONFORMSTO,
        required=False,
        title=i18n.LABEL_DCT_CONFORMSTO,
        vocabulary='pkan.dcatapde.vocabularies.DCTStandard',
    )

    form.widget(
        'dct_format',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_DCT_MEDIATYPEOREXTENT,
        content_type_title=i18n.LABEL_DCT_FORMAT,
        initial_path='/formats/',
    )
    dct_format = schema.Choice(
        description=i18n.HELP_DCT_FORMAT,
        required=False,
        title=i18n.LABEL_DCT_FORMAT,
        vocabulary='pkan.dcatapde.vocabularies.DCTMediaTypeOrExtent',
    )

    form.widget(
        'dcat_mediatype',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_DCT_MEDIATYPEOREXTENT,
        content_type_title=i18n.LABEL_DCAT_MEDIATYPE,
        initial_path='/formats/',
    )

    dcat_mediatype = schema.Choice(
        description=i18n.HELP_DACT_MEDIATYPE,
        required=False,
        title=i18n.LABEL_DCAT_MEDIATYPE,
        vocabulary='pkan.dcatapde.vocabularies.DCTMediaTypeOrExtent',
    )

    dct_issued = schema.Date(
        required=False,
        title=i18n.LABEL_DCT_ISSUED,
    )

    dct_modified = schema.Date(
        required=False,
        title=i18n.LABEL_DCT_MODIFIED,
    )


@implementer(IDCATDistribution)
class DCATDistribution(Container, DCATMixin):
    """DCATDistribution Content Type."""

    portal_type = constants.CT_DCAT_DISTRIBUTION
    content_schema = IDCATDistribution
    _namespace = 'dcat'
    _ns_class = 'distribution'

    dct_title = I18NTextProperty(IDCATDistribution['dct_title'])
    dct_description = I18NTextProperty(IDCATDistribution['dct_description'])
    dcatde_plannedAvailability = I18NTextProperty(
        IDCATDistribution['dcatde_plannedAvailability'],
    )
    dcatde_licenseAttributionByText = I18NTextProperty(
        IDCATDistribution['dcatde_licenseAttributionByText'],
    )
    dcat_byteSize = I18NTextProperty(IDCATDistribution['dcat_byteSize'])

    def Title(self):
        return self.title_from_title_field()

    def Description(self):
        return unicode(self.dct_description)


class DCATDistributionDefaultFactory(DexterityFactory):
    """Custom DX factory for DCATDistribution."""

    def __init__(self):
        self.portal_type = constants.CT_DCAT_DISTRIBUTION

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.dcat_distribution import clean_distribution
        data, errors = clean_distribution(**kw)

        return super(
            DCATDistributionDefaultFactory,
            self,
        ).__call__(*args, **data)
