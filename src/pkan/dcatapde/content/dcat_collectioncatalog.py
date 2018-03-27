# -*- coding: utf-8 -*-
"""DCATCatalog Content Type."""

from pkan.dcatapde import constants
from pkan.dcatapde.content.dcat_catalog import DCATCatalog
from pkan.dcatapde.content.dcat_catalog import IDCATCatalog
from plone.dexterity.factory import DexterityFactory
from ps.zope.i18nfield.fieldproperty import I18NTextProperty
from zope.interface import implementer


class IDCATCollectionCatalog(IDCATCatalog):
    """Marker interface and Dexterity Python Schema for
    DCATCollectionCatalog."""


@implementer(IDCATCollectionCatalog)
class DCATCollectionCatalog(DCATCatalog):
    """DCATCatalog Content Type."""

    portal_type = constants.CT_DCAT_COLLECTION_CATALOG
    content_schema = IDCATCollectionCatalog
    _namespace = 'dcat'
    _ns_class = 'catalog'

    dct_title = I18NTextProperty(IDCATCatalog['dct_title'])
    dct_description = I18NTextProperty(IDCATCatalog['dct_description'])

    def Title(self):
        return self.title_from_title_field()

    def Description(self):
        return unicode(self.dct_description)


class DCATCollectionCatalogDefaultFactory(DexterityFactory):
    """Custom DX factory for DCATCatalog."""

    def __init__(self):
        self.portal_type = constants.CT_DCAT_CATALOG

    def __call__(self, *args, **kw):
        from pkan.dcatapde.api.dcat_catalog import clean_catalog

        data, errors = clean_catalog(**kw)

        return super(
            DCATCollectionCatalogDefaultFactory,
            self,
        ).__call__(*args, **data)
