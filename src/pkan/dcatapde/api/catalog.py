# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import CT_Catalog
from pkan.dcatapde.content.catalog import Catalog
from pkan.dcatapde.content.catalog import ICatalog
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_catalog(**data):

    test_catalog = Catalog()

    for attr in data:
        setattr(test_catalog, attr, data[attr])

    errors = getValidationErrors(ICatalog, test_catalog)

    return data, errors



# Add Methods
def add_catalog(context, **data):
    data, errors = clean_catalog(**data)

    catalog = create(container=context, type=CT_Catalog, **data)

    return catalog


# Get Methods

# Delete Methods

# Related Methods
