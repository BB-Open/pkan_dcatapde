# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import DataGridFieldFactory
from pkan.dcatapde import _
from pkan.dcatapde.api.harvester import add_harvester
from pkan.dcatapde.api.harvester import delete_harvester
from pkan.dcatapde.api.harvester import get_all_harvester
from pkan.dcatapde.api.harvester import get_harvester_folder
from pkan.dcatapde.config.interfaces import IConfigHarvesterSchema
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.autoform.form import AutoExtensibleForm
from plone.z3cform import layout
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import ActionExecutionError
from zope.interface import Invalid


class HarvesterForm(AutoExtensibleForm, form.Form):
    ''' Define Form handling

    This form can be accessed as http://yoursite/@@my-form

    '''
    schema = IConfigHarvesterSchema
    ignoreContext = True

    fields = field.Fields(IConfigHarvesterSchema)
    fields['harvester'].widgetFactory = DataGridFieldFactory

    label = _(u'Harverster Configuration')

    def __init__(self, *args, **kwargs):
        self.description = _(u'''Configure your Harvester here.''')

        super(HarvesterForm, self).__init__(*args, **kwargs)

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        harvester_folder = get_harvester_folder()

        if not harvester_folder:
            raise ActionExecutionError(
                Invalid('Please create Harvester-Folder first'))

        harvester = data['harvester']

        harvester_url = []

        for element in harvester:
            harvester_url.append(element['url'])

        created_harvester = get_all_harvester()
        created_harvester_url = []

        for obj in created_harvester:
            created_harvester_url.append(obj.url)

        all = set(created_harvester_url + harvester_url)

        for url in all:
            if url in created_harvester_url and url not in harvester_url:
                index = created_harvester_url.index(url)
                delete_harvester(created_harvester[index])
            elif url in harvester_url and url not in created_harvester_url:
                index = harvester_url.index(url)
                add_harvester(self.context, **harvester[index])
            else:
                index = created_harvester_url.index(url)
                harvester_obj = (created_harvester[index])
                index = harvester_url.index(url)
                data = harvester[index]
                harvester_obj.type = data['type']

        self.successMessage = _(u'Stored Changes')
        IStatusMessage(self.request).addStatusMessage(
            self.successMessage)

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        '''User cancelled. Redirect back to the front page.
        '''


class HarvesterView(BrowserView):
    '''
    View which wrap the settings form using ControlPanelFormWrapper to a
    HTML boilerplate frame.
    '''

    def __call__(self, *args, **kwargs):
        view_factor = layout.wrap_form(HarvesterForm,
                                       ControlPanelFormWrapper)
        view = view_factor(self.context, self.request)
        return view()

    def parent_panel_url(self):
        return '{url}/@@pkan-dcatapde-config'.format(
            url=self.context.absolute_url()
        )


class MainControlPanelView(BrowserView):
    label = _(u'Pkan Dcatapde Main Config')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def actions(self):
        cstate = self.context.restrictedTraverse('plone_context_state')
        actions = cstate.actions('pkan_dcatapde_config')
        return actions
