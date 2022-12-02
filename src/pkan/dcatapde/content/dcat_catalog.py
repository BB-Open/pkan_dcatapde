# -*- coding: utf-8 -*-
"""DCATCatalog Content Type."""
import datetime

import zope.schema as schema
from pkan.widgets.ajaxselect import AjaxSelectAddFieldWidget
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives as form
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


class IDCATCatalog(model.Schema, IDCAT):
    """Marker interface and Dexterity Python Schema for DCATCatalog."""

    # Fieldsets
    # -------------------------------------------------------------------------
    model.fieldset(
        'linking',
        label=i18n.FIELDSET_RELATIONS,
        fields=[
            'dct_hasPart',
            'dct_isPartOf',
            'dct_spatial',
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

    form.widget(
        'dct_publisher',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_FOAF_AGENT,
        content_type_title=i18n.LABEL_DCT_PUBLISHER,
        initial_path='/publishers/',
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

    foaf_homepage = schema.URI(
        required=False,
        title=i18n.LABEL_FOAF_HOMEPAGE,
    )

    form.widget(
        'dct_language',
        AjaxSelectFieldWidget,
        vocabulary='pkan.dcatapde.AvailableContentLanguageVocabulary',
    )
    dct_language = schema.List(
        required=False,
        title=i18n.LABEL_DCT_LANGUAGE,
        value_type=schema.Choice(
            vocabulary='pkan.dcatapde.AvailableContentLanguageVocabulary',
        ),
    )

    form.widget(
        'dcat_themeTaxonomy',
        AjaxSelectAddFieldWidget,
        display_deprecated=True,
        content_type=constants.CT_SKOS_CONCEPTSCHEME,
        content_type_title=i18n.LABEL_DCT_THEMETAXONOMY,
        initial_path='/conceptschemes/',
    )
    dcat_themeTaxonomy = schema.Choice(
        description=i18n.HELP_DCT_THEMETAXONOMY,
        required=False,
        title=i18n.LABEL_DCT_THEMETAXONOMY,
        vocabulary='pkan.dcatapde.vocabularies.SKOSConceptScheme',
    )

    # Optional
    # -------------------------------------------------------------------------
    form.widget(
        'dct_rights',
        AjaxSelectAddFieldWidget,
        display_deprecated=True,
        content_type=constants.CT_DCT_RIGHTSSTATEMENT,
        content_type_title=i18n.LABEL_DCT_RIGHTS,
        initial_path='/rights/',
    )
    dct_rights = schema.Choice(
        description=i18n.HELP_DCT_RIGHTS,
        required=False,
        title=i18n.LABEL_DCT_RIGHTS,
        vocabulary='pkan.dcatapde.vocabularies.DCTRightsStatement',
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

    form.widget(
        'dct_hasPart',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_DCAT_CATALOG,
        content_type_title=i18n.LABEL_DCT_HASPART,
        initial_path='/',
    )
    dct_hasPart = schema.Choice(
        description=i18n.HELP_DCT_HASPART,
        required=False,
        title=i18n.LABEL_DCT_HASPART,
        vocabulary='pkan.dcatapde.vocabularies.DCATCatalog',
    )

    form.widget(
        'dct_isPartOf',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_DCAT_CATALOG,
        content_type_title=i18n.LABEL_DCT_ISPARTOF,
        initial_path='/',
    )
    dct_isPartOf = schema.Choice(
        description=i18n.HELP_DCT_ISPARTOF,
        required=False,
        title=i18n.LABEL_DCT_ISPARTOF,
        vocabulary='pkan.dcatapde.vocabularies.DCATCatalog',
    )

    form.widget(
        'dct_spatial',
        AjaxSelectAddFieldWidget,
        content_type=constants.CT_DCT_LOCATION,
        content_type_title=i18n.LABEL_DCT_SPATIAL,
        initial_path='/locations/',
    )
    dct_spatial = schema.List(
        description=i18n.HELP_DCT_SPATIAL,
        required=False,
        title=i18n.LABEL_DCT_SPATIAL,
        value_type=schema.Choice(
            vocabulary='pkan.dcatapde.vocabularies.DCTLocation',
        ),
    )


@implementer(IDCATCatalog)
class DCATCatalog(Container, DCATMixin):
    """DCATCatalog Content Type."""

    portal_type = constants.CT_DCAT_CATALOG
    content_schema = IDCATCatalog
    _namespace = 'dcat'
    _ns_class = 'Catalog'

    dct_title = I18NTextProperty(IDCATCatalog['dct_title'])
    dct_description = I18NTextProperty(IDCATCatalog['dct_description'])

    def Title(self):
        return self.title_from_title_field()

    def Description(self):
        return self.desc_from_desc_field()
