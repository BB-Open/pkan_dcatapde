# -*- coding: utf-8 -*-
from pkan.dcatapde import constants
# get functions
from pkan.dcatapde.constants import ACTIVE_STATE
from pkan.dcatapde.constants import CT_HARVESTER
from pkan.dcatapde.constants import DEACTIVE_STATE
from pkan.dcatapde.constants import PKAN_STATE_NAME
from pkan.dcatapde.constants import PROVIDER_ADMIN_PERM
from pkan.dcatapde.constants import PROVIDER_ADMIN_ROLE
from pkan.dcatapde.constants import PROVIDER_CHIEF_EDITOR_PERM
from pkan.dcatapde.constants import PROVIDER_CHIEF_EDITOR_ROLE
from pkan.dcatapde.constants import PROVIDER_DATA_EDITOR_ROLE
from pkan.dcatapde.constants import PRVIDER_DATA_EDITOR_PERM
from plone import api
from plone.api.exc import UserNotFoundError
from plone.api.user import has_permission


def get_user_roles():
    """
    Retrieve the roles of the current user
    :return:
    """
    roles = api.user.get_roles(user=api.user.get_current())
    return roles


def is_admin():
    """
    Check if the current user is SiteAdministrator
    :return:
    """
    roles = get_user_roles()
    return 'Manager' in roles


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
        pt_check = new_portal_type == constants.CT_PLONE_SITE
        if not new_portal_type or pt_check or not obj:
            return None

    return obj


def get_all_harvester_folder():
    """Find all HarvesterFolder"""
    portal = api.portal.get()
    if not portal:
        return None
    res = api.content.find(**{'portal_type': constants.CT_HARVESTER_FOLDER})
    folder = []
    for brain in res:
        folder.append(brain.getObject())
    return folder


def get_all_transfer_folder():
    """Find all HarvesterFolder"""
    portal = api.portal.get()
    if not portal:
        return None
    res = api.content.find(**{'portal_type': constants.CT_TRANSFER_FOLDER})
    folder = []
    for brain in res:
        folder.append(brain.getObject())
    return folder


def query_active_objects(query, portal_type, context=None):
    params = {
        'portal_type': portal_type,
        'sort_on': 'sortable_title',
        PKAN_STATE_NAME: ACTIVE_STATE,
    }
    query.update(params)

    catalog = api.portal.get_tool('portal_catalog')
    brains = list(catalog(query))

    harvester = get_ancestor(context, CT_HARVESTER)
    if context and harvester:
        # add objects from the same harvest
        query['path'] = '/'.join(harvester.getPhysicalPath())
        brains += list(catalog(query))
    elif context:
        # add objects of the same user
        try:
            current = api.user.get_current()
            roles = api.user.get_roles(user=current, obj=context)
        except UserNotFoundError:
            return brains
        check_admin = PROVIDER_ADMIN_ROLE in roles
        check_editor = PROVIDER_DATA_EDITOR_ROLE in roles
        check_chief = PROVIDER_CHIEF_EDITOR_ROLE in roles
        if check_admin or check_editor or check_chief:
            query[PKAN_STATE_NAME] = DEACTIVE_STATE
            new_brains = catalog(query)
            for brain in new_brains:
                obj = brain.getObject()
                perm = has_permission(PRVIDER_DATA_EDITOR_PERM, obj=obj,
                                      user=current)
                perm = perm or has_permission(PROVIDER_ADMIN_PERM, obj=obj,
                                              user=current)
                perm = perm or has_permission(PROVIDER_CHIEF_EDITOR_PERM,
                                              obj=obj,
                                              user=current)

                if perm:
                    brains.append(brain)

    return brains


def query_objects_no_pkanstate(query, portal_type, context=None):
    params = {
        'portal_type': portal_type,
        'sort_on': 'sortable_title',
    }
    query.update(params)

    catalog = api.portal.get_tool('portal_catalog')
    brains = list(catalog(query))

    return brains
