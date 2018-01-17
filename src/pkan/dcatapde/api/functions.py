# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from plone import api


def get_foafagent_context():
    # todo context should not be the site
    context = api.portal.get()
    return context


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
