# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.browser.add_views.default_add_view import PkanDefaultAddForm
from pkan.dcatapde.browser.add_views.default_add_view import PkanDefaultAddView
from z3c.form import button


class HarvesterAddForm(PkanDefaultAddForm):
    """
    Add Form for Havester including Run and preview
    """

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):
        super(HarvesterAddForm, self).handleAdd(self, action)

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        super(HarvesterAddForm, self).handleCancel(self, action)


class HarvesterAddView(PkanDefaultAddView):
    """Default add view."""

    form = HarvesterAddForm
