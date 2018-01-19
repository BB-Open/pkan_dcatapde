# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from plone import api


def restore_user(old_sm):
    # restore security context of user
    if old_sm:
        setSecurityManager(old_sm)


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

    portal = api.portal.get()
    # start using as admin
    newSecurityManager(portal, portal.getOwner())
    return old_sm
