# -*- coding: utf-8 -*-
"""Work with dct_mediatypeorextent."""

from pkan.dcatapde.constants import CT_DctMediatypeorextent
from pkan.dcatapde.content.dct_mediatypeorextent import Dct_Mediatypeorextent
from pkan.dcatapde.content.dct_mediatypeorextent import IDct_Mediatypeorextent
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_dct_mediatypeorextent(**data):
    """Clean dct_mediatypeorextent."""
    test_obj = Dct_Mediatypeorextent()

    # test object must have an id
    test_obj.id = 'test'
    test_obj.title = 'test'

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(IDct_Mediatypeorextent, test_obj)

    return data, errors


# Add Methods
def add_dct_mediatypeorextent(context, **data):
    """Add a new dct_mediatypeorextent."""
    data, errors = clean_dct_mediatypeorextent(**data)
    result = create(container=context, type=CT_DctMediatypeorextent, **data)

    return result

# Get Methods

# Delete Methods

# Related Methods
