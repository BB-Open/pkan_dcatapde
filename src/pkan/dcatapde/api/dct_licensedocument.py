# -*- coding: utf-8 -*-
"""Work with dct_licensedocument."""

from pkan.dcatapde.constants import CT_DctLicenseDocument
from pkan.dcatapde.content.dct_licensedocument import Dct_Licensedocument
from pkan.dcatapde.content.dct_licensedocument import IDct_Licensedocument
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_dct_licensedocument(**data):
    """Clean dct_licensedocument."""
    test_license = Dct_Licensedocument()

    for attr in data:
        setattr(test_license, attr, data[attr])

    errors = getValidationErrors(IDct_Licensedocument, test_license)

    return data, errors


# Add Methods
def add_dct_licensedocument(context, **data):
    """Add a new dct_licensedocument."""
    data, errors = clean_dct_licensedocument(**data)
    result = create(container=context, type=CT_DctLicenseDocument, **data)

    return result

# Get Methods

# Delete Methods

# Related Methods
