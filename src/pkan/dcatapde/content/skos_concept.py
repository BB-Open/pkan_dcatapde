# -*- coding: utf-8 -*-
"""SKOSConcept Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_SKOS_CONCEPT
from pkan.dcatapde.content.base import DCATMixin
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from zope import schema
from zope.interface import implementer


class ISKOSConcept(model.Schema):
    """Marker interface and DX Python Schema for SKOSConcept."""

    dct_title = I18NTextLine(
        required=True,
        title=_(u'Title'),
    )

    dct_description = I18NText(
        required=False,
        title=_(u'Description'),
    )

    skos_inScheme = schema.URI(
        required=True,
        title=_(u'Concept scheme URI'),
        description=_(u'URI to the concept scheme'),
    )

    rdfs_isDefinedBy = schema.URI(
        required=True,
        title=_(u'Description URI'),
        description=_(u'The URI describing this concept'),
    )


@implementer(ISKOSConcept)
class SKOSConcept(Item, DCATMixin):
    """SKOSConcept Content Type."""

    portal_type = 'skos_concept'
    _namespace = 'skos'
    _ns_class = 'concept'


class SKOSConceptDefaultFactory(DexterityFactory):
    """Custom DX factory for SKOSConcept."""

    def __init__(self):
        self.portal_type = CT_SKOS_CONCEPT

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.skos_concept import \
            clean_skos_concept
        data, errors = clean_skos_concept(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
