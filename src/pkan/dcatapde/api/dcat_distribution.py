# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import CT_DCAT_DISTRIBUTION
from pkan.dcatapde.content.dcat_distribution import DCATDistribution
from pkan.dcatapde.content.dcat_distribution import IDCATDistribution
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_distribution(**data):
    test_obj = DCATDistribution()

    # test object must have an id
    test_obj.id = 'test'
    test_obj.title = 'test'

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(IDCATDistribution, test_obj)

    return data, errors


# Add Methods
def add_distribution(context, **data):
    data, errors = clean_distribution(**data)
    dist = create(container=context, type=CT_DCAT_DISTRIBUTION, **data)

    return dist

# Get Methods

# Delete Methods

# Related Methods
