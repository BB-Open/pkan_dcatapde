# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import DataGridFieldFactory
from pkan.dcatapde import _
from pkan.dcatapde import constants
from pkan.dcatapde.content.fielddefaultfactory import ConfigFieldDefaultFactory
from pkan.dcatapde.content.harvester_entity import HarvesterEntity
from pkan.dcatapde.content.harvester_entity import IHarvesterEntity
from plone import api
from z3c.form import field
from zope.schema import getFieldNamesInOrder
from zope.schema import getValidationErrors


# clean methods
def clean_entity(**data):
    """Clean entityconfig."""

    test_obj = HarvesterEntity()
    test_obj.id = constants.HARVESTER_ENTITY_ID
    test_obj.title = constants.HARVESTER_ENTITY_TITLE

    for attr in data:
        setattr(test_obj, attr, data[attr])

    errors = getValidationErrors(IHarvesterEntity, test_obj)

    return data, errors


# add methods
def add_harvester_entity(context, **data):
    """Add a harvester entity config."""
    assert get_entity_config(context) is None, \
        _('API: Cannot create second entity config for harvester')

    data, errors = clean_entity(**data)

    # harvesting_type = context.harvesting_type(context)
    # used_cts = harvesting_type.get_used_cts()
    #
    # for ct in used_cts:
    #     if ct in CT_ENTITY_RELATION:
    #         if CT_ENTITY_RELATION[ct] in data:
    #             ct_fields = add_missing_entities(
    #                 data[CT_ENTITY_RELATION[ct]],
    #                 ct=ct,
    #                 context=context
    #             )
    #         else:
    #             ct_fields = add_missing_entities(
    #                 [],
    #                 ct=ct,
    #                 context=context
    #             )
    #         data[CT_ENTITY_RELATION[ct]] = ct_fields

    harvester_entity_config = api.content.create(
        container=context,
        type=constants.CT_HARVESTER_ENTITY,
        title=constants.HARVESTER_ENTITY_TITLE,
        id=constants.HARVESTER_ENTITY_ID,
        **data)

    return harvester_entity_config


# get methods
def get_entity_config(harvester):
    """Get a entity config."""
    if harvester and constants.HARVESTER_ENTITY_ID in harvester:
        return harvester[constants.HARVESTER_ENTITY_ID]

    return None


# related methods
def add_missing_entities(entitys, ct=None, context=None):
    """Add missing entitys."""
    factory = ConfigFieldDefaultFactory(ct, context=context)
    required_entitys = factory()

    if not entitys:
        return sort_entities(required_entitys)

    return []


def sort_entities(entities):
    return entities


def update_form_fields(context):
    # harvester = get_ancestor(context, CT_HARVESTER)

    selected = getFieldNamesInOrder(IHarvesterEntity)

    # if harvester:
    #     harvesting_type = harvester.harvesting_type(harvester)
    #     used_cts = harvesting_type.get_used_cts()
    #
    #     for ct in CT_ENTITY_RELATION.keys():
    #         if ct not in used_cts:
    #             selected.remove(CT_ENTITY_RELATION[ct])

    fields = field.Fields(IHarvesterEntity).select(*selected)

    for schema_field in fields:
        if 'fields' in schema_field:
            fields[schema_field].widgetFactory = DataGridFieldFactory

    return fields
