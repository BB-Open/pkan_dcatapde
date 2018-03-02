# -*- coding: utf-8 -*-
"""Work with dct_rightsstatement."""
from pkan.dcatapde import constants
from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.content.dct_rightsstatement import DCTRightsStatement
from pkan.dcatapde.content.dct_rightsstatement import IDCTRightsStatement
from plone import api
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_dct_rightsstatement(**data):
    """Clean dct_rightsstatement."""
    test_license = DCTRightsStatement()

    # test object must have an id
    test_license.id = 'test'
    test_license.title = 'test'

    for attr in data:
        setattr(test_license, attr, data[attr])

    errors = getValidationErrors(IDCTRightsStatement, test_license)

    return data, errors


def find_dct_rightsstatement(data):
    """Find a given on a search pattern equivalent to an create dataset"""
    catalog = api.portal.get_tool('portal_catalog')

    search_data = {}

    # add the portal type
    search_data['portal_type'] = DCTRightsStatement.portal_type
    search_data['id'] = data['adms_identifier']

    results = catalog.searchResults(**search_data)

    if len(results) >= 1:
        result = results[0].getObject()
    elif len(results) == 0:
        result = None

    return result


# Add Methods
def add_dct_rightsstatement(context, **data):
    """Add a new dct_rightsstatement."""
    context = get_dctrightsstatement_context()

    data, errors = clean_dct_rightsstatement(**data)

    result = find_dct_rightsstatement(data)
    if not result:
        # No such license exists create a new one
        result = create(
            container=context,
            id=data['adms_identifier'],
            type=CT_DCT_LICENSEDOCUMENT,
            **data)

    return result


# Get Methods
def get_dctrightsstatement_context():
    """Get content for an foafagent."""
    # fix: context should not be the site
    site = api.portal.get()
    context = site.get(constants.FOLDER_LICENSES)
    return context


# Delete Methods

# Related Methods
