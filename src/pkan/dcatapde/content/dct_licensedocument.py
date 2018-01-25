# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DctLicenseDocument
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from zope.interface import implementer

import zope.schema as schema


class IDct_Licensedocument(model.Schema):
    """ Marker interface and Dexterity Python Schema for Dct_Licensedocument
    """

    rdf_about = schema.URI(
         title=_(u'Access URI'),
         required=True
    )


@implementer(IDct_Licensedocument)
class Dct_Licensedocument(Item):
    """
    """
    portal_type = 'dct_licensedocument'
    namespace_class = 'dct:licensedocument'


class DctLicensedocumentDefaultFactory(DexterityFactory):

    def __init__(self):
        self.portal_type = CT_DctLicenseDocument

    def __call__(self, *args, **kw):
        # TODO: get context and maybe change it
        from pkan.dcatapde.api.dct_licensedocument import \
            clean_dct_licensedocument
        data, errors = clean_dct_licensedocument(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
