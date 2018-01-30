# -*- coding: utf-8 -*-
"""Post install import steps for pkan.dcatapde."""

from pkan.dcatapde import constants
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


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def add_default_folders(context):
    """Add default folders on first install."""
    portal = _get_navigation_root(context)
    add_licenses_folder(portal)


def add_licenses_folder(portal):
    """Add licenses folder."""
    licenses = portal.get(constants.FOLDER_LICENSES)
    if not licenses:
        licenses = api.content.create(
            container=portal,
            type='Folder',
            id=constants.FOLDER_LICENSES,
            title=u'Licenses',
        )
        allowed_types = [constants.CT_DCT_LICENSE_DOCUMENT]
        _setup_constrains(licenses, allowed_types)
        _publish(licenses)


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
