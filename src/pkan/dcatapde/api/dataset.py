# -*- coding: utf-8 -*-
"""Work with Datasets."""

from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.content.dcat_dataset import DCATDataset
from pkan.dcatapde.content.dcat_dataset import IDCATDataset
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_dataset(**data):
    """Clean datasets."""
    test_dataset = DCATDataset()

    # test object must have an id
    test_dataset.id = 'test'
    test_dataset.title = 'test'

    for attr in data:
        setattr(test_dataset, attr, data[attr])

    errors = getValidationErrors(IDCATDataset, test_dataset)

    return data, errors


# Add Methods
def add_dataset(context, **data):
    """Add a new dataset."""
    data, errors = clean_dataset(**data)

    dataset = create(container=context, type=CT_DCAT_DATASET, **data)

    return dataset

# Get Methods

# Delete Methods

# Related Methods
