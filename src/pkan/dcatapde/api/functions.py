# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from pkan.dcatapde import constants
from plone import api
from zope.component.hooks import getSite


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


def work_as_admin():
    """
    Analog to doing an "su root"
    :param request:
    :return:
    """
    current = api.user.get_current()
    old_sm = getSecurityManager()
    if current.id == 'admin':
        return old_sm
    # Save old user security context

    portal = getSite()
    # start using as admin
    newSecurityManager(portal, portal.getOwner())
    return old_sm


def restore_user(old_sm):
    # restore security context of user
    if old_sm:
        setSecurityManager(old_sm)
