# -*- coding: utf-8 -*-
from plone.dexterity.browser import edit
from plone.dexterity.interfaces import IDexterityEditForm
from plone.z3cform import layout
from z3c.form import button
from zope.interface import classImplements

from pkan.dcatapde import _
from pkan.dcatapde import utils
from pkan.dcatapde.content.harvester import IHarvester


class HarvesterEditForm(edit.DefaultEditForm):
    schema = IHarvester

    def __init__(self, context, request, ti=None):
        super(HarvesterEditForm, self).__init__(context, request)
        utils.set_request_annotations('pkan.vocabularies.context', context)

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):
        super(HarvesterEditForm, self).handleApply(self, action)

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        super(HarvesterEditForm, self).handleCancel(self, action)


HarvesterEditView = layout.wrap_form(HarvesterEditForm)
classImplements(HarvesterEditView, IDexterityEditForm)
