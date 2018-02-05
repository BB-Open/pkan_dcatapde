# -*- coding: utf-8 -*-
"""Work with harvester."""
from collective.z3cform.datagridfield import DataGridFieldFactory
from pkan.dcatapde import _
from pkan.dcatapde import constants
from pkan.dcatapde.api.functions import get_ancestor
from pkan.dcatapde.constants import CT_HARVESTER
from pkan.dcatapde.content.fielddefaultfactory import ConfigFieldDefaultFactory
from pkan.dcatapde.content.harvester import Harvester
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.content.harvester_field_config import CT_FIELD_RELATION
from pkan.dcatapde.content.harvester_field_config import HarvesterFieldConfig
from pkan.dcatapde.content.harvester_field_config import IHarvesterFieldConfig
from pkan.dcatapde.content.harvesterfolder import Harvesterfolder
from pkan.dcatapde.content.harvesterfolder import IHarvesterfolder
from plone import api
from z3c.form import field
from zope.component.hooks import getSite
from zope.schema import getValidationErrors


# Data Cleaning Methods
def clean_harvester(**data):
    """Clean harvester."""
    data['title'] = data['url']

    test_obj = Harvester()

    # test object must have an id
    test_obj.id = 'test'
    test_obj.title = 'test'

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


def clean_fieldconfig(**data):
    """Clean fieldconfig."""

    test_obj = HarvesterFieldConfig()
    test_obj.id = constants.HARVESTER_FIELD_CONFIG_ID
    test_obj.title = constants.HARVESTER_FIELD_CONFIG_TITLE

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(IHarvesterFieldConfig, test_obj)

    return data, errors


# Add Methods
def add_harvester_field_config(context, **data):
    """Add a harvester field config."""
    assert get_field_config(context) is None, \
        _('API: Cannot create second field config for harvester')

    data, errors = clean_fieldconfig(**data)

    harvesting_type = context.harvesting_type(context)
    used_cts = harvesting_type.get_used_cts()

    for ct in used_cts:
        if ct in CT_FIELD_RELATION:
            if CT_FIELD_RELATION[ct] in data:
                ct_fields = add_missing_fields(data[CT_FIELD_RELATION[ct]],
                                               ct=ct)
            else:
                ct_fields = add_missing_fields([], ct=ct)
            data[CT_FIELD_RELATION[ct]] = ct_fields

    harvester_field_config = api.content.create(
        container=context,
        type=constants.CT_HARVESTER_FIELD_CONFIG,
        title=constants.HARVESTER_FIELD_CONFIG_TITLE,
        id=constants.HARVESTER_FIELD_CONFIG_ID,
        **data)

    return harvester_field_config


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
    msg = _('API: Cannot create second harvester_folder folder')
    assert get_harvester_folder() is None, msg

    data, errors = clean_harvesterfolder(**data)

    # set id and title, title for presentation and id for addressing the object
    harvester_folder = api.content.create(
        container=context,
        type=constants.CT_HARVESTER_FOLDER,
        title=constants.HARVESTER_FOLDER_TITLE,
        id=constants.HARVESTER_FOLDER_ID,
        **data)

    return harvester_folder


# Get Methods
def get_field_config(harvester):
    """Get a field config."""
    if harvester and constants.HARVESTER_FIELD_CONFIG_ID in harvester:
        return harvester[constants.HARVESTER_FIELD_CONFIG_ID]

    return None


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
    """Find the folder where the harvester_folder live."""
    portal = getSite()
    if not portal:
        return None
    catalog = portal.portal_catalog
    res = catalog.searchResults({'portal_type': constants.CT_HARVESTER})
    harvester = []
    for brain in res:
        harvester.append(brain.getObject())
    return harvester


# Delete Methods
def delete_harvester(object):
    """Remove a harvester."""
    parent = get_harvester_folder()
    parent.manage_delObjects([object.getId()])


# Related Methods
def add_missing_fields(fields, ct=None):
    """Add missing fields."""
    factory = ConfigFieldDefaultFactory(ct)
    required_fields = factory()

    if not fields:
        return sort_fields(required_fields)

    required_dcat_fields = {}
    available_fields = []
    unneeded_fields = []

    for element in required_fields:
        required_dcat_fields[element['dcat_field']] = element

    for element in fields:
        available_fields.append(element['dcat_field'])

    for element in available_fields:
        if element in required_dcat_fields:
            del required_dcat_fields[element]
        else:
            # here we collect fields which get unrequired
            # after setting a context
            unneeded_fields.append(element)

    wanted_fields = []

    # remove unrequired fields if source_field is not set
    for conf_field in fields:
        dcat_field = conf_field['dcat_field']
        source_field = conf_field['source_field']

        if source_field or (dcat_field not in unneeded_fields):
            wanted_fields.append(conf_field)

    fields = wanted_fields + required_dcat_fields.values()

    return sort_fields(fields)


def sort_fields(fields):
    field_dict = {}

    for conf_field in fields:
        if conf_field['dcat_field'] not in field_dict:
            field_dict[conf_field['dcat_field']] = [conf_field]
        else:
            field_dict[conf_field['dcat_field']].append(conf_field)

    fields = []

    for x in sorted(field_dict.iterkeys()):
        fields += field_dict[x]

    return fields


def update_field_config_form_fields(context):
    harvester = get_ancestor(context, CT_HARVESTER)

    selected = []

    if harvester:
        harvesting_type = harvester.harvesting_type(harvester)
        used_cts = harvesting_type.get_used_cts()

        for ct in used_cts:
            if ct in CT_FIELD_RELATION:
                selected.append(CT_FIELD_RELATION[ct])

    fields = field.Fields(IHarvesterFieldConfig).select(*selected)

    for schema_field in fields:
        if 'fields' in schema_field:
            fields[schema_field].widgetFactory = DataGridFieldFactory

    return fields
