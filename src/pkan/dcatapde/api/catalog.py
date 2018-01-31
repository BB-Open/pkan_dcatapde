# -*- coding: utf-8 -*-
"""Work with Catalogs."""

from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.content.dcat_catalog import DCATCatalog
from pkan.dcatapde.content.dcat_catalog import IDCATCatalog
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_catalog(**data):
    """Clean Catalogs."""
    test_catalog = DCATCatalog()

    # test object must have an id
    test_catalog.id = 'test'
    test_catalog.title = 'test'

    for attr in data:
        setattr(test_catalog, attr, data[attr])

    errors = getValidationErrors(IDCATCatalog, test_catalog)

    return data, errors


# Add Methods
def add_catalog(context, **data):
    """Add a new Catalog."""
    data, errors = clean_catalog(**data)

    catalog = create(container=context, type=CT_DCAT_CATALOG, **data)

    return catalog

# Get Methods

# Delete Methods

# Related Methods
