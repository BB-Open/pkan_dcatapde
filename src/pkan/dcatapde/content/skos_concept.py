# -*- coding: utf-8 -*-
"""SKOSConcept Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from pkan.dcatapde.content.base import IDCAT
from pkan.dcatapde.i18n import HELP_FOAF_DEPICTION
from plone.dexterity.content import Item
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope import schema
from zope.interface import implementer


class ISKOSConcept(model.Schema, IDCAT):
    """Marker interface and DX Python Schema for SKOSConcept."""

    # Mandatory
    # -------------------------------------------------------------------------
    dct_title = I18NTextLine(
        required=True,
        title=i18n.LABEL_DCT_TITLE,
    )

    dct_description = I18NText(
        required=False,
        title=i18n.LABEL_DCT_DESCRIPTION,
    )

    skos_inScheme = schema.URI(
        description=i18n.HELP_SKOS_INSCHEME,
        required=True,
        title=i18n.LABEL_SKOS_INSCHEME,
    )

    rdfs_isDefinedBy = schema.URI(
        description=i18n.HELP_RDFS_ISDEFINEDBY,
        required=False,
        title=i18n.LABEL_RDFS_ISDEFINEDBY,
    )

    foaf_depiction = schema.TextLine(
        required=False,
        title=_(u'Icon class for category'),
        description=_(HELP_FOAF_DEPICTION),

    )


@implementer(ISKOSConcept)
class SKOSConcept(Item, DCATMixin):
    """SKOSConcept Content Type."""

    portal_type = constants.CT_SKOS_CONCEPT
    content_schema = ISKOSConcept
    _namespace = 'skos'
    _ns_class = 'Concept'

    dct_title = I18NTextProperty(ISKOSConcept['dct_title'])
    dct_description = I18NTextProperty(ISKOSConcept['dct_description'])

    def Title(self):
        return self.title_from_title_field()

    def Description(self):
        return self.desc_from_desc_field()
