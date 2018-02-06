# -*- coding: utf-8 -*-
"""SKOSConxwptScheme Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_SKOS_CONCEPTSCHEME
from pkan.dcatapde.content.base import DCATMixin
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from zope import schema
from zope.interface import implementer


class ISKOSConceptScheme(model.Schema):
    """Marker interface and DX Python Schema for SKOSConceptScheme."""

    dct_title = I18NTextLine(
        required=True,
        title=_(u'Title'),
    )

    dct_description = I18NText(
        required=False,
        title=_(u'Description'),
    )

    rdf_about = schema.URI(
        required=True,
        title=_(u'URI'),
        description=_(u'Where is this concept scheme defined'),
    )


@implementer(ISKOSConceptScheme)
class SKOSConceptScheme(Item, DCATMixin):
    """SKOSConceptScheme Content Type."""

    portal_type = 'skos_conceptscheme'
    _namespace = 'skos'
    _ns_class = 'conceptscheme'


class SKOSConceptSchemeDefaultFactory(DexterityFactory):
    """Custom DX factory for SKOSConceptScheme."""

    def __init__(self):
        self.portal_type = CT_SKOS_CONCEPTSCHEME

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.skos_conceptscheme import \
            clean_skos_conceptscheme
        data, errors = clean_skos_conceptscheme(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
