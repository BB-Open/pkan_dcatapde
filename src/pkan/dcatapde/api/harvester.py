# -*- coding: utf-8 -*-
"""Work with harvester."""
from pkan.dcatapde import constants
from pkan.dcatapde.content.harvester import Harvester
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.content.harvesterfolder import Harvesterfolder
from pkan.dcatapde.content.harvesterfolder import IHarvesterfolder
from plone import api
from zope.component.hooks import getSite
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_harvester(**data):
    """Clean harvester."""
    if not data:
        return data, ()

    if 'title' not in data:
        data['title'] = data['url']

    test_obj = Harvester()

    # test object must have an id
    test_obj.id = 'test'

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(IHarvester, test_obj)

    return data, errors


def clean_harvesterfolder(**data):
    """Clean Harvesterfolder."""
    test_obj = Harvesterfolder()

    test_obj.id = constants.HARVESTER_FOLDER_ID
    test_obj.title = constants.HARVESTER_FOLDER_TITLE

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(IHarvesterfolder, test_obj)

    return data, errors


# Add Methods
def add_harvester(context, **data):
    """Add a harvester."""
    folder = get_harvester_folder()

    data, errors = clean_harvester(**data)

    harvester = api.content.create(
        container=folder,
        type=constants.CT_HARVESTER,
        **data)

    return harvester


def add_harvester_folder(context, **data):
    """Add a harvester folder."""

    data, errors = clean_harvesterfolder(**data)

    # set id and title, title for presentation and id for addressing the object
    if 'title' not in data:
        data['title'] = constants.HARVESTER_FOLDER_TITLE
    if 'id' not in data:
        data['id'] = constants.HARVESTER_FOLDER_ID
    harvester_folder = api.content.create(
        container=context,
        type=constants.CT_HARVESTER_FOLDER,
        **data)

    return harvester_folder


# Get Methods
def get_harvester_folder():
    """Find the folder where the harvester_folder live."""
    portal = getSite()
    if not portal:
        return None
    catalog = portal.portal_catalog
    res = catalog.searchResults({'portal_type': constants.CT_HARVESTER_FOLDER})
    if len(res) != 0:
        return res[0].getObject()
    else:
        return None


def get_all_harvester():
    """Get all harvester,"""
    portal = getSite()
    if not portal:
        return None
    catalog = portal.portal_catalog
    res = catalog.searchResults({'portal_type': constants.CT_HARVESTER})
    harvester = []
    for brain in res:
        harvester.append(brain.getObject())
    return harvester


def get_all_harvester_folder():
    """Find all HarvesterFolder"""
    portal = getSite()
    if not portal:
        return None
    catalog = portal.portal_catalog
    res = catalog.searchResults({'portal_type': constants.CT_HARVESTER_FOLDER})
    folder = []
    for brain in res:
        folder.append(brain.getObject())
    return folder


# Delete Methods
def delete_harvester(object):
    """Remove a harvester."""
    parent = get_harvester_folder()
    parent.manage_delObjects([object.getId()])


# Related Methods
