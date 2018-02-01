# -*- coding: utf-8 -*-
"""PKAN Control Panel."""

from pkan.dcatapde import _
from pkan.dcatapde import interfaces
from pkan.dcatapde.browser.controlpanel import base
from plone.app.registry.browser import controlpanel
from zope.interface import implementer


@implementer(interfaces.IPKANSettings)
class PKANSettingsEditForm(base.SelfHealingRegistryEditForm):
    """PKAN Settings Form."""

    schema = interfaces.IPKANSettings
    label = _(u'PKAN Settings')
    description = _(u'Manage all PKAN specific settings.')

    def updateFields(self):
        super(PKANSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(PKANSettingsEditForm, self).updateWidgets()


class PKANBaseSettingsPanelView(controlpanel.ControlPanelFormWrapper):
    """PKAN Settings Control Panel."""

    form = PKANSettingsEditForm
