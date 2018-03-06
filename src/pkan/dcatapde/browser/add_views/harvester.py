# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.browser.add_views.default_add_view import PkanDefaultAddForm
from pkan.dcatapde.browser.add_views.default_add_view import PkanDefaultAddView
from pkan.dcatapde.browser.harvester_entity.preview import PreviewFormMixin
from z3c.form import button


class HarvesterAddForm(PkanDefaultAddForm, PreviewFormMixin):
    """
    Add Form for Havester including Run and preview
    """
    query_attr = 'top_node_sparql'
    url_attr = 'url'
    type_attr = 'source_type'

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):
        super(HarvesterAddForm, self).handleAdd(self, action)

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        super(HarvesterAddForm, self).handleCancel(self, action)

    @button.buttonAndHandler(_(u'Run'))
    def handle_run(self, action):
        self.handle_preview(ignore_context=True)


class HarvesterAddView(PkanDefaultAddView):
    """Default add view."""

    form = HarvesterAddForm
