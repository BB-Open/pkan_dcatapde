# -*- coding: utf-8 -*-
"""Work with dct_location."""

from pkan.dcatapde.constants import CT_DCT_LOCATION
from pkan.dcatapde.content.dct_location import DCTLocation
from pkan.dcatapde.content.dct_location import IDCTLocation
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean(**data):
    """Clean dct_location."""
    test_license = DCTLocation()

    # test object must have an id
    test_license.id = 'test'
    test_license.title = 'test'

    for attr in data:
        setattr(test_license, attr, data[attr])

    errors = getValidationErrors(IDCTLocation, test_license)

    return data, errors


# Add Methods
def add_dct_location(context, **data):
    """Add a new dct_location."""
    data, errors = clean(**data)
    result = create(container=context, type=CT_DCT_LOCATION, **data)

    return result

# Get Methods

# Delete Methods

# Related Methods
