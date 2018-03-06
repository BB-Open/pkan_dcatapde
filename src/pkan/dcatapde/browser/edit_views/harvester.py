# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde import utils
from pkan.dcatapde.browser.harvester_entity.preview import PreviewFormMixin
from pkan.dcatapde.content.harvester import IHarvester
from plone.dexterity.browser import edit
from z3c.form import button


class HarvesterEdit(edit.DefaultEditForm, PreviewFormMixin):

    schema = IHarvester
    query_attr = 'top_node_sparql'
    url_attr = 'url'
    type_attr = 'source_type'

    def __init__(self, context, request, ti=None):
        super(HarvesterEdit, self).__init__(context, request)
        utils.set_request_annotations('pkan.vocabularies.context', context)

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):
        super(HarvesterEdit, self).handleApply(self, action)

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        super(HarvesterEdit, self).handleCancel(self, action)

    @button.buttonAndHandler(_(u'Run'))
    def handle_run(self, action):
        self.handle_preview(ignore_context=True)
