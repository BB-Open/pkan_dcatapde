# -*- coding: utf-8 -*-
"""Configuration Views."""

from Products.Five.browser import BrowserView

from pkan.dcatapde import _


class MainControlPanelView(BrowserView):
    """Control Panel View."""

    label = _(u'Pkan Dcatapde Main Config')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def actions(self):
        cstate = self.context.restrictedTraverse('plone_context_state')
        actions = cstate.actions('pkan_dcatapde_config')
        return actions
