# -*- coding: utf-8 -*-
"""Post install import steps for pkan.dcatapde."""

from pkan.dcatapde import constants as c
from plone import api
from plone.app.dexterity.behaviors import constrains
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    """Hidden GS profiles."""

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            'pkan.dcatapde:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    add_default_folders(context)
    set_constraints(context)


def pre_install(context):
    """Pre install script"""
    # Do something at the beginning of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def add_default_folders(context):
    """Add default folders on first install."""
    portal = _get_navigation_root(context)
    for folder_name, folder_type in c.MANDATORY_FOLDERS.items():
        add_folder(portal, folder_name, folder_type)


def add_folder(portal, folder_name, folder_type):
    """Add a folder for the exclusive addition of certain CTs"""
    folder = portal.get(folder_name)
    if not folder:
        types = api.portal.get_tool(name='portal_types')
        fti = types.getTypeInfo(folder_type)
        fti.global_allow = True
        folder = api.content.create(
            container=portal,
            type=folder_type,
            id=folder_name,
            title=unicode(folder_name),
        )
        fti.global_allow = False
        _publish(folder)


def set_constraints(context):
    """Set content type constraints."""


def _get_navigation_root(context):
    """Find the correct navigation root."""
    documents = api.content.find(portal_type='Document', id='front-page')
    if len(documents) == 0:
        return api.portal.get()
    front_page = documents[0].getObject()

    return api.portal.get_navigation_root(front_page)


def _publish(content):
    """Publish the object if it hasn't been published."""
    if api.content.get_state(obj=content) != 'published':
        api.content.transition(obj=content, transition='publish')
        return True
    return False


def _setup_constrains(container, allowed_types):
    """Set allowed types as constraint for a given container."""
    behavior = ISelectableConstrainTypes(container)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setImmediatelyAddableTypes(allowed_types)
    return True
