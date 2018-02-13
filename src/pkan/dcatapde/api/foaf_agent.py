# -*- coding: utf-8 -*-
"""Work with FOAFAgents."""

from pkan.dcatapde.constants import CT_FOAF_AGENT
from pkan.dcatapde.content.foaf_agent import FOAFAgent
from pkan.dcatapde.content.foaf_agent import IFOAFAgent
from plone import api
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_foafagent(**data):
    """Clean foafagent."""
    test_obj = FOAFAgent()

    # test object must have an id
    test_obj.id = 'test'
    test_obj.title = 'test'

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(IFOAFAgent, test_obj)

    return data, errors


def find_foaf_agent(data):
    """Find a given on a search pattern equivalent to an create dataset"""
    catalog = api.portal.get_tool('portal_catalog')

    search_data = data.copy()
    # strip the data of legacy fields like title and description
    for key in ['title', 'description']:
        try:
            del search_data[key]
        except KeyError:
            pass

    # add the portal type
    search_data['portal_type'] = FOAFAgent.portal_type

    results = catalog.searchResults(**search_data)

    if len(results) > 1:
        result = results[0]
    elif len(results) == 0:
        result = None
    else:
        result = results

    return result


# Add Methods
def add_foafagent(context, **data):
    """Add a new foafagent."""
    context = get_foafagent_context()

    data, errors = clean_foafagent(**data)

    agent = find_foaf_agent(data)
    if not agent:
        # no such agent exits create a new one
        agent = api.content.create(
            container=context,
            type=CT_FOAF_AGENT,
            **data)

    return agent


# Get Methods
def get_foafagent_context():
    """Get content for an foafagent."""
    # fix: context should not be the site
    context = api.portal.get()
    return context


# Delete Methods


# Related Methods
