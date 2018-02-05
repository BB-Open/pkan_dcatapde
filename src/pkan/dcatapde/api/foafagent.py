# -*- coding: utf-8 -*-
"""Work with FOAFAgents."""

from pkan.dcatapde.constants import CT_FOAF_AGENT
from pkan.dcatapde.content.foaf_agent import FOAFagent
from pkan.dcatapde.content.foaf_agent import IFOAFagent
from plone import api
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_foafagent(**data):
    """Clean foafagent."""
    test_obj = FOAFagent()

    # test object must have an id
    test_obj.id = 'test'
    test_obj.title = 'test'

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(IFOAFagent, test_obj)

    return data, errors


# Add Methods
def add_foafagent(context, **data):
    """Add a new foafagent."""
    data, errors = clean_foafagent(**data)

    foaf = api.content.create(container=context, type=CT_FOAF_AGENT, **data)

    return foaf


# Get Methods
def get_foafagent_context():
    """Get content for an foafagent."""
    # fix: context should not be the site
    context = api.portal.get()
    return context

# Delete Methods

# Related Methods
