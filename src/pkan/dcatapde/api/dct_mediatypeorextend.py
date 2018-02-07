# -*- coding: utf-8 -*-
"""Work with dct_mediatypeorextent."""

from pkan.dcatapde.constants import CT_DCAT_MEDIATYPEOREXTEND
from pkan.dcatapde.content.dct_mediatypeorextent import DCTMediaTypeOrExtent
from pkan.dcatapde.content.dct_mediatypeorextent import IDCTMediaTypeOrExtent
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_dct_mediatypeorextent(**data):
    """Clean dct_mediatypeorextent."""
    test_obj = DCTMediaTypeOrExtent()

    # test object must have an id
    test_obj.id = 'test'
    test_obj.title = 'test'

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(IDCTMediaTypeOrExtent, test_obj)

    return data, errors


# Add Methods
def add_dct_mediatypeorextent(context, **data):
    """Add a new dct_mediatypeorextent."""
    data, errors = clean_dct_mediatypeorextent(**data)
    result = create(container=context, type=CT_DCAT_MEDIATYPEOREXTEND, **data)

    return result

# Get Methods

# Delete Methods

# Related Methods
