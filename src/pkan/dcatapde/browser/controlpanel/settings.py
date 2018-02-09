# -*- coding: utf-8 -*-
"""PKAN Control Panel."""

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from pkan.dcatapde import interfaces
from pkan.dcatapde.browser.controlpanel import base
from plone import api
from plone.app.registry.browser import controlpanel
from plone.protect.utils import addTokenToUrl
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
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

    buttons = base.SelfHealingRegistryEditForm.buttons.copy()
    handlers = base.SelfHealingRegistryEditForm.handlers.copy()

    @button.buttonAndHandler(
        i18n.BUTTON_IMPORT_DCT_LICENSEDOCUMENT,
        name='import_dct_licensedocument',
    )
    def handle_import_dct_licensedocument(self, action):
        url = '/'.join([
            api.portal.get().absolute_url(),
            constants.FOLDER_LICENSES,
            '@@update_licenses',
        ])
        self.request.response.redirect(addTokenToUrl(url))
        return u''

    @button.buttonAndHandler(
        i18n.BUTTON_IMPORT_SKOS_CONCEPT,
        name='import_skos_concept',
    )
    def handle_import_skos_concept(self, action):
        url = '/'.join([
            api.portal.get().absolute_url(),
            constants.FOLDER_CONCEPTS,
            '@@update_themes',
        ])
        self.request.response.redirect(addTokenToUrl(url))
        return u''


class PKANImportSettingsPanelView(controlpanel.ControlPanelFormWrapper):
    """PKAN Import Settings Control Panel."""

    form = PKANImportSettingsEditForm
    index = ViewPageTemplateFile('templates/controlpanel_layout_imports.pt')
