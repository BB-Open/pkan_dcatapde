# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import CT_Distribution
from pkan.dcatapde.content.distribution import Distribution
from pkan.dcatapde.content.distribution import IDistribution
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_distribution(**data):
    test_obj = Distribution()

    # test object must have an id
    test_obj.id = 'test'
    test_obj.title = 'test'

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(IDistribution, test_obj)

    return data, errors


# Add Methods
def add_distribution(context, **data):
    data, errors = clean_distribution(**data)
    dist = create(container=context, type=CT_Distribution, **data)

    return dist

# Get Methods

# Delete Methods

# Related Methods
