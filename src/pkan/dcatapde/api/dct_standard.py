# -*- coding: utf-8 -*-
"""Work with dct_standard."""

from pkan.dcatapde.constants import CT_DCT_STANDARD
from pkan.dcatapde.content.dct_standard import DCTStandard
from pkan.dcatapde.content.dct_standard import IDCTStandard
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean(**data):
    """Clean dct_standard."""
    item = DCTStandard()

    # test object must have an id
    item.id = 'test'
    item.title = 'test'

    for attr in data:
        setattr(item, attr, data[attr])

    errors = getValidationErrors(IDCTStandard, item)

    return data, errors


# Add Methods
def add_dct_standard(context, **data):
    """Add a new dct_standard."""
    data, errors = clean(**data)
    result = create(container=context, type=CT_DCT_STANDARD, **data)

    return result

# Get Methods

# Delete Methods

# Related Methods
