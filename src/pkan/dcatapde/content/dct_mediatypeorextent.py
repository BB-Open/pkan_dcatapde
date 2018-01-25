# -*- coding: utf-8 -*-
from pkan.dcatapde.api.dct_mediatypeorextend import add_dct_mediatypeorextent
from pkan.dcatapde.constants import CT_DctMediatypeorextent
from plone.dexterity.content import Item
from plone.dexterity.factory import DexterityFactory
from plone.supermodel import model
from pkan.dcatapde import _
import zope.schema as schema
from zope.interface import implementer


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
        data = add_dct_mediatypeorextent(None, dry_run=True, **kw)
        folder = DexterityFactory.__call__(self, *args, **data)

        return folder