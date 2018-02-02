# -*- coding: utf-8 -*-
"""Work with dct_mediatypeorextent."""

from pkan.dcatapde.constants import CT_SCOS_CONCEPTSCHEME
from pkan.dcatapde.content.scos_conceptscheme import ISCOSConceptScheme
from pkan.dcatapde.content.scos_conceptscheme import SCOSConceptScheme
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_dct_mediatypeorextent(**data):
    """Clean dct_mediatypeorextent."""
    test_obj = SCOSConceptScheme()

    # test object must have an id
    test_obj.id = 'test'
    test_obj.title = 'test'

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(ISCOSConceptScheme, test_obj)

    return data, errors


# Add Methods
def add_dct_mediatypeorextent(context, **data):
    """Add a new dct_mediatypeorextent."""
    data, errors = clean_dct_mediatypeorextent(**data)
    result = create(container=context, type=CT_SCOS_CONCEPTSCHEME, **data)

    return result

# Get Methods

# Delete Methods

# Related Methods
