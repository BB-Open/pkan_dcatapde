# -*- coding: utf-8 -*-
"""Work with dct_licensedocument."""

from pkan.dcatapde.constants import CT_DCT_LICENSE_DOCUMENT
from pkan.dcatapde.content.dct_licensedocument import DCTLicenseDocument
from pkan.dcatapde.content.dct_licensedocument import IDCTLicenseDocument
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_dct_licensedocument(**data):
    """Clean dct_licensedocument."""
    test_license = DCTLicenseDocument()

    # test object must have an id
    test_license.id = 'test'
    test_license.title = 'test'

    for attr in data:
        setattr(test_license, attr, data[attr])

    errors = getValidationErrors(IDCTLicenseDocument, test_license)

    return data, errors


# Add Methods
def add_dct_licensedocument(context, **data):
    """Add a new dct_licensedocument."""
    data, errors = clean_dct_licensedocument(**data)
    result = create(container=context, type=CT_DCT_LICENSE_DOCUMENT, **data)

    return result

# Get Methods

# Delete Methods

# Related Methods
