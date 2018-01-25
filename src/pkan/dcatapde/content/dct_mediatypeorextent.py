# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.constants import CT_DctMediatypeorextent
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from zope.interface import implementer

import zope.schema as schema


class IDct_Mediatypeorextent(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Dct_Mediatypeorextent
    """

    rdf_about = schema.URI(
         title=_(u'Access URI'),
         required=True
    )


@implementer(IDct_Mediatypeorextent)
class Dct_Mediatypeorextent(Item):
    """
    """
    portal_type = 'dct_licensedocument'
    namespace_class = 'dct:licensedocument'


class DctMediatypeorextentDefaultFactory(DexterityFactory):

    def __init__(self):
        self.portal_type = CT_DctMediatypeorextent

    def __call__(self, *args, **kw):
        # TODO: get context and maybe change it
        from pkan.dcatapde.api.dct_mediatypeorextend import \
            clean_dct_mediatypeorextent
        data, errors = clean_dct_mediatypeorextent(**kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder
