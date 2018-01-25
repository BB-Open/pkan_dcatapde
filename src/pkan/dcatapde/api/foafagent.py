# -*- coding: utf-8 -*-
"""Work with FOAFAgents."""

from pkan.dcatapde.constants import CT_Foafagent
from pkan.dcatapde.content.foafagent import Foafagent
from pkan.dcatapde.content.foafagent import IFoafagent
from plone import api
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_foafagent(**data):
    """Clean foafagent."""
    test_obj = Foafagent()

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(IFoafagent, test_obj)

    return data, errors


# Add Methods
def add_foafagent(context, **data):
    """Add a new foafagent."""
    data, errors = clean_foafagent(**data)

    foaf = api.content.create(container=context, type=CT_Foafagent, **data)

    return foaf


# Get Methods
def get_foafagent_context():
    """Get content for an foafagent."""
    # todo context should not be the site
    context = api.portal.get()
    return context

# Delete Methods

# Related Methods
