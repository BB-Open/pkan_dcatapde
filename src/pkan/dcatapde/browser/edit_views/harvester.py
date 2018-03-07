# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde import utils
from pkan.dcatapde.browser.harvester_entity.preview import PreviewFormMixin
from pkan.dcatapde.content.harvester import IHarvester
from plone.dexterity.browser import edit
from plone.dexterity.interfaces import IDexterityEditForm
from plone.z3cform import layout
from z3c.form import button
from zope.interface import classImplements


class HarvesterEditForm(edit.DefaultEditForm, PreviewFormMixin):

    schema = IHarvester
    query_attr = 'top_node_sparql'
    url_attr = 'url'
    type_attr = 'source_type'

    def __init__(self, context, request, ti=None):
        super(HarvesterEditForm, self).__init__(context, request)
        utils.set_request_annotations('pkan.vocabularies.context', context)

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):
        super(HarvesterEditForm, self).handleApply(self, action)

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        super(HarvesterEditForm, self).handleCancel(self, action)

    @button.buttonAndHandler(_(u'Run'))
    def handle_run(self, action):
        self.handle_preview(ignore_context=True)


HarvesterEditView = layout.wrap_form(HarvesterEditForm)
classImplements(HarvesterEditView, IDexterityEditForm)
