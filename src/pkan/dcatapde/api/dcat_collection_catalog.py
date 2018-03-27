# -*- coding: utf-8 -*-
"""Work with CollectionCatalogs."""

from pkan.dcatapde.constants import CT_DCAT_COLLECTION_CATALOG
from pkan.dcatapde.content.dcat_collectioncatalog import DCATCollectionCatalog
from pkan.dcatapde.content.dcat_collectioncatalog import IDCATCollectionCatalog
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_collection_catalog(**data):
    """Clean CollectionCatalogs."""
    test_catalog = DCATCollectionCatalog()

    # test object must have an id
    test_catalog.id = 'test'
    test_catalog.title = 'test'

    for attr in data:
        setattr(test_catalog, attr, data[attr])

    errors = getValidationErrors(IDCATCollectionCatalog, test_catalog)

    return data, errors


# Add Methods
def add_collection_catalog(context, **data):
    """Add a new CollectionCatalog."""
    data, errors = clean_collection_catalog(**data)

    catalog = create(container=context,
                     type=CT_DCAT_COLLECTION_CATALOG,
                     **data)

    return catalog

# Get Methods

# Delete Methods

# Related Methods
