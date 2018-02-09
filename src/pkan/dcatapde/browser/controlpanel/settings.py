# -*- coding: utf-8 -*-
"""PKAN Control Panel."""

from pkan.dcatapde import i18n
from pkan.dcatapde import interfaces
from pkan.dcatapde.browser.controlpanel import base
from plone.app.registry.browser import controlpanel
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer


@implementer(interfaces.IPKANBaseSettings)
class PKANBaseSettingsEditForm(base.SelfHealingRegistryEditForm):
    """PKAN Settings Form."""

    description = i18n.HELP_SETTINGS_BASE
    label = i18n.LABEL_SETTINGS_BASE
    schema = interfaces.IPKANBaseSettings


class PKANBaseSettingsPanelView(controlpanel.ControlPanelFormWrapper):
    """PKAN Settings Control Panel."""

    form = PKANBaseSettingsEditForm
    index = ViewPageTemplateFile('templates/controlpanel_layout_base.pt')


@implementer(interfaces.IPKANFolderSettings)
class PKANFolderSettingsEditForm(base.SelfHealingRegistryEditForm):
    """PKAN Folder Settings Form."""

    description = i18n.HELP_SETTINGS_FOLDERS
    label = i18n.LABEL_SETTINGS_FOLDERS
    schema = interfaces.IPKANFolderSettings


class PKANFolderSettingsPanelView(controlpanel.ControlPanelFormWrapper):
    """PKAN Folder Settings Control Panel."""

    form = PKANFolderSettingsEditForm
    index = ViewPageTemplateFile('templates/controlpanel_layout_folders.pt')


@implementer(interfaces.IPKANImportSettings)
class PKANImportSettingsEditForm(base.SelfHealingRegistryEditForm):
    """PKAN Import Settings Form."""

    description = i18n.HELP_SETTINGS_IMPORTS
    label = i18n.LABEL_SETTINGS_IMPORTS
    schema = interfaces.IPKANImportSettings


class PKANImportSettingsPanelView(controlpanel.ControlPanelFormWrapper):
    """PKAN Import Settings Control Panel."""

    form = PKANImportSettingsEditForm
    index = ViewPageTemplateFile('templates/controlpanel_layout_imports.pt')
