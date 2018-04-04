# -*- coding: utf-8 -*-
from pkan.dcatapde import constants
from pkan.dcatapde.harvesting.field_adapter.interfaces import IFieldProcessor
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import ComponentLookupError
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.schema import getFieldsInOrder


# security related functions

# vocabulary related functions
def get_terms_for_ct(CT, prefix='', required=False):
    terms = []
    try:
        schema = getUtility(IDexterityFTI,
                            name=CT).lookupSchema()
    except ComponentLookupError:
        return terms
    fields = getFieldsInOrder(schema)
    for field_name, field in fields:
        adapter = IFieldProcessor(field)

        terms += adapter.get_terms_for_vocab(CT,
                                             field_name,
                                             prefix=prefix,
                                             required=required)

    return terms


# get functions
def get_parent(context):
    """
    get the parent return None if no parent is found
    """
    if context is None:
        return None

    aq_parent = getattr(context, 'aq_parent', None)

    if not aq_parent:
        uid = context.UID()
        context = api.content.get(UID=uid)
        if context is None:
            return None

    obj = context.aq_parent

    portal_type = getattr(obj, 'portal_type', None)

    if not portal_type:
        return None
    return obj


def get_ancestor(context, portal_type):
    """
    get a parent with the given type for the context where current user is
    return None if no parent is found
    """
    obj = context

    if not obj:
        return None

    old_portal_type = getattr(obj, 'portal_type', None)
    if not old_portal_type:
        return None

    while obj.portal_type != portal_type:
        obj = get_parent(obj)
        new_portal_type = getattr(obj, 'portal_type', None)
        if (not new_portal_type or
                (new_portal_type == constants.CT_PLONE_SITE) or
                not obj):
            return None

    return obj


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
