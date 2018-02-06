# -*- coding: utf-8 -*-
"""Work with skos_conceptscheme."""

from pkan.dcatapde.constants import CT_SKOS_CONCEPTSCHEME
from pkan.dcatapde.content.skos_conceptscheme import ISKOSConceptScheme
from pkan.dcatapde.content.skos_conceptscheme import SKOSConceptScheme
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_skos_conceptscheme(**data):
    """Clean skos_conceptscheme."""
    test_obj = SKOSConceptScheme()

    # test object must have an id
    test_obj.id = 'test'
    test_obj.title = 'test'

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(ISKOSConceptScheme, test_obj)

    return data, errors


# Add Methods
def add_skos_conceptscheme(context, **data):
    """Add a new _skos_conceptscheme."""
    data, errors = clean_skos_conceptscheme(**data)
    result = create(container=context, type=CT_SKOS_CONCEPTSCHEME, **data)

    return result

# Get Methods

# Delete Methods

# Related Methods
