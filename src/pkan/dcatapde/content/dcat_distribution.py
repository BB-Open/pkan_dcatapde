# -*- coding: utf-8 -*-
"""DCATDistribution Content Type."""
import datetime

from pkan.widgets.ajaxselect import AjaxSelectAddFieldWidget
from plone.autoform import directives as form
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.dexterity.content import Container
from plone.namedfile.field import NamedFile
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope import schema
from zope.interface import implementer
from zope.interface import invariant, Invalid

from pkan.dcatapde import constants, _
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.content.base import IDCAT


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
        display_deprecated=True,
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

    local_file = NamedFile(
        required=False,
        title=i18n.LABEL_LOCAL_FILE,
    )

    read_permission(dcatde_plannedAvailability='pkan.dcatapde.Admin')
    write_permission(dcatde_plannedAvailability='pkan.dcatapde.Admin')
    dcatde_plannedAvailability = I18NText(
        required=False,
        title=i18n.LABEL_DCATDE_PLANNED_AVAILABLITY,
    )

    dcatde_licenseAttributionByText = I18NText(
        required=False,
        title=i18n.LABEL_DCATDE_LICENSEATTRIBUTIONBYTEXT,
    )

    read_permission(dcat_byteSize='pkan.dcatapde.Admin')
    write_permission(dcat_byteSize='pkan.dcatapde.Admin')
    dcat_byteSize = I18NTextLine(
        required=False,
        title=i18n.LABEL_DCAT_BYTESIZE,
    )

    read_permission(dct_conformsTo='pkan.dcatapde.Admin')
    write_permission(dct_conformsTo='pkan.dcatapde.Admin')
    form.widget(
        'dct_conformsTo',
        AjaxSelectAddFieldWidget,
        display_deprecated=True,
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
        display_deprecated=True,
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

    read_permission(dcat_mediaType='pkan.dcatapde.Admin')
    write_permission(dcat_mediaType='pkan.dcatapde.Admin')
    form.widget(
        'dcat_mediaType',
        AjaxSelectAddFieldWidget,
        display_deprecated=True,
        content_type=constants.CT_DCT_MEDIATYPEOREXTENT,
        content_type_title=i18n.LABEL_DCAT_MEDIATYPE,
        initial_path='/formats/',
    )

    dcat_mediaType = schema.Choice(
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
        default=datetime.date.today(),
    )

    @invariant
    def address_invariant(data):
        if not data.local_file and not data.dcat_accessURL:
            raise Invalid(_(u'You have to provide a file or a dcat_accessURL.'))


@implementer(IDCATDistribution)
class DCATDistribution(Container, DCATMixin):
    """DCATDistribution Content Type."""

    portal_type = constants.CT_DCAT_DISTRIBUTION
    content_schema = IDCATDistribution
    _namespace = 'dcat'
    _ns_class = 'Distribution'

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
        return self.desc_from_desc_field()


def distribution_add_handler(sender, event):
    if sender.local_file:
        download_postfix = '/@@download/local_file'
        sender.dcat_downloadURL = sender.absolute_url() \
            + download_postfix
        sender.dcat_accessURL = sender.absolute_url()
