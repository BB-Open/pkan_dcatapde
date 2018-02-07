# -*- coding: utf-8 -*-
"""SKOSConcept Content Type."""

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde.content.base import DCATMixin
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope import schema
from zope.interface import implementer


class ISKOSConcept(model.Schema):
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
        required=True,
        title=i18n.LABEL_RDFS_ISDEFINEDBY,
    )


@implementer(ISKOSConcept)
class SKOSConcept(Item, DCATMixin):
    """SKOSConcept Content Type."""

    portal_type = constants.CT_SKOS_CONCEPT
    _namespace = 'skos'
    _ns_class = 'concept'

    dct_title = I18NTextProperty(ISKOSConcept['dct_title'])
    dct_description = I18NTextProperty(ISKOSConcept['dct_description'])

    def Title(self):
        return unicode(self.dct_title)

    def Description(self):
        return self.dct_description


class SKOSConceptDefaultFactory(DexterityFactory):
    """Custom DX factory for SKOSConcept."""

    def __init__(self):
        self.portal_type = constants.CT_SKOS_CONCEPT

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.skos_concept import \
            clean_skos_concept
        data, errors = clean_skos_concept(**kw)

        return super(
            SKOSConceptDefaultFactory,
            self,
        ).__call__(*args, **data)
