# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde import constants
from pkan.dcatapde.content.harvester_field_config import FieldDefaultFactory
from plone.dexterity.utils import createContentInContainer
from zope.component.hooks import getSite


def get_harvester_folder():
    '''
    Find the folder where the harvester_folder live
    '''
    portal = getSite()
    if not portal:
        return None
    catalog = portal.portal_catalog
    res = catalog.searchResults({'portal_type': constants.CT_HarvesterFolder})
    if len(res) != 0:
        return res[0].getObject()
    else:
        return None


def get_all_harvester():
    '''
    Find the folder where the harvester_folder live
    '''
    portal = getSite()
    if not portal:
        return None
    catalog = portal.portal_catalog
    res = catalog.searchResults({'portal_type': constants.CT_Harvester})
    harvester = []
    for brain in res:
        harvester.append(brain.getObject())
    return harvester


def add_harvester_folder(context, dry_run=False):
    assert get_harvester_folder() is None, \
        _('API: Cannot create second harvester_folder folder')

    # set id and title, title for presentation and id for addressing the object
    if not dry_run:
        harvester_folder = createContentInContainer(
            context,
            constants.CT_HarvesterFolder,
            title=constants.HARVESTER_FOLDER_TITLE,
            id=constants.HARVESTER_FOLDER_ID
        )

        return harvester_folder


def delete_harvester(object):
    parent = get_harvester_folder()
    parent.manage_delObjects([object.getId()])


def add_harvester(context, dry_run=False, **data):
    folder = get_harvester_folder()

    data['title'] = data['url']

    if not dry_run:
        harvester = createContentInContainer(folder,
                                             constants.CT_Harvester,
                                             **data)

        add_harvester_field_config(harvester)

        return harvester


def get_field_config(harvester):
    return harvester[constants.HARVESTER_FIELD_CONFIG_ID]


def add_harvester_field_config(context, dry_run=False, **data):
    assert get_field_config(context) is None, \
        _('API: Cannot create second field config for harvester')

    if 'fields' not in data:
        data['fields'] = add_missing_fields(context, [])

    if not dry_run:
        harvester_field_config = createContentInContainer(
            context,
            constants.CT_HarvesterFieldConfig,
            title=constants.HARVESTER_FIELD_CONFIG_TITLE,
            id=constants.HARVESTER_FIELD_CONFIG_ID,
            **data
        )

        return harvester_field_config


def add_missing_fields(context, fields):
    required_fields = FieldDefaultFactory(context)

    if not fields:
        return required_fields

    required_dcat_fields = {}
    available_fields = []

    for element in required_fields:
        required_dcat_fields[element['dcat_field']] = element

    for element in fields:
        available_fields.append(element['dcat_field'])

    for element in available_fields:
        if element in required_dcat_fields:
            del required_dcat_fields[element]

    fields += required_dcat_fields.values()

    return fields
