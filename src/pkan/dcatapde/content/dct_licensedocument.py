# -*- coding: utf-8 -*-
"""Dct_Licensedocument Content Type."""

from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DctLicenseDocument
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IDct_Licensedocument(model.Schema):
    """Marker interface and DX Python Schema for Dct_Licensedocument."""

    rdf_about = schema.URI(
        required=True,
        title=_(u'Access URI'),
    )


@implementer(IDct_Licensedocument)
class Dct_Licensedocument(Item):
    """Dct_Licensedocument Content Type."""

    portal_type = 'dct_licensedocument'
    namespace_class = 'dct:licensedocument'


class DctLicensedocumentDefaultFactory(DexterityFactory):
    """Custom DX factory for Dct_Licensedocument."""

    def __init__(self):
        self.portal_type = CT_DctLicenseDocument

    def __call__(self, *args, **kw):
        # Fix: get context and maybe change it
        from pkan.dcatapde.api.dct_licensedocument import \
            clean_dct_licensedocument
        data, errors = clean_dct_licensedocument(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
