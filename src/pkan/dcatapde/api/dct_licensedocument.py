# -*- coding: utf-8 -*-
"""Work with dct_licensedocument."""
from pkan.dcatapde import constants
from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.content.dct_licensedocument import DCTLicenseDocument
from pkan.dcatapde.content.dct_licensedocument import IDCTLicenseDocument
from plone import api
from plone.api.content import create
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_dct_licensedocument(**data):
    """Clean dct_licensedocument."""
    test_license = DCTLicenseDocument()

    # test object must have an id
    test_license.id = 'test'
    test_license.title = 'test'

    for attr in data:
        setattr(test_license, attr, data[attr])

    errors = getValidationErrors(IDCTLicenseDocument, test_license)

    return data, errors


def find_dct_licensedocument(data):
    """Find a given on a search pattern equivalent to an create dataset"""
    catalog = api.portal.get_tool('portal_catalog')

    search_data = {}

    # add the portal type
    search_data['portal_type'] = DCTLicenseDocument.portal_type
    search_data['id'] = data['adms_identifier']

    results = catalog.searchResults(**search_data)

    if len(results) >= 1:
        result = results[0].getObject()
    elif len(results) == 0:
        result = None

    return result


# Add Methods
def add_dct_licensedocument(context, **data):
    """Add a new dct_licensedocument."""
    context = get_dctlicensedocument_context()

    data, errors = clean_dct_licensedocument(**data)

    result = find_dct_licensedocument(data)
    if not result:
        # No such license exists create a new one
        result = create(
            container=context,
            id=data['adms_identifier'],
            type=CT_DCT_LICENSEDOCUMENT,
            **data)

    return result


# Get Methods
def get_dctlicensedocument_context():
    """Get content for an foafagent."""
    # fix: context should not be the site
    site = api.portal.get()
    context = site.get(constants.FOLDER_LICENSES)
    return context


# Delete Methods

# Related Methods
