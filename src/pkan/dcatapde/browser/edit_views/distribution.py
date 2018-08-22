# -*- coding: utf-8 -*-
from pkan.dcatapde import utils
from pkan.dcatapde.content.dcat_distribution import IDCATDistribution
from plone.dexterity.browser import edit
from plone.dexterity.interfaces import IDexterityEditForm
from plone.z3cform import layout
from zope.interface import classImplements


class DistributionEditForm(edit.DefaultEditForm):

    schema = IDCATDistribution

    def __init__(self, context, request, ti=None):
        super(DistributionEditForm, self).__init__(context, request)
        utils.set_request_annotations('pkan.vocabularies.context', context)

    def applyChanges(self, data):
        local_file_obj = data['local_file']
        if local_file_obj is not None:
            download_postfix = '/@@download/local_file'
            data['dcat_downloadURL'] = self.context.absolute_url() \
                + download_postfix
        super(DistributionEditForm, self).applyChanges(data)
        pass

#    @button.buttonAndHandler(_(u'Save'), name='save')
#    def handleApply(self, action):
#        super(HarvesterEditForm, self).handleApply(self, action)

#    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
#    def handleCancel(self, action):
#        super(HarvesterEditForm, self).handleCancel(self, action)


DistributionEditView = layout.wrap_form(DistributionEditForm)
classImplements(DistributionEditView, IDexterityEditForm)
