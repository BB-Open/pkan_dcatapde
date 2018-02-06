# -*- coding: utf-8 -*-
"""Work with skos_concept."""

from pkan.dcatapde.constants import CT_SKOS_CONCEPT
from pkan.dcatapde.content.skos_concept import ISKOSConcept
from pkan.dcatapde.content.skos_concept import SKOSConcept
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_skos_concept(**data):
    """Clean skos_concept."""
    test_obj = SKOSConcept()

    # test object must have an id
    test_obj.id = 'test'
    test_obj.title = 'test'

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(ISKOSConcept, test_obj)

    return data, errors


# Add Methods
def add_skos_concept(context, **data):
    """Add a new _skos_concept."""
    data, errors = clean_skos_concept(**data)
    result = create(container=context, type=CT_SKOS_CONCEPT, **data)

    return result

# Get Methods

# Delete Methods

# Related Methods
