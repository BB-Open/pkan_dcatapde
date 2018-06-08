# -*- coding: utf-8 -*-

from plone.app.contentmenu.interfaces import IActionsSubMenuItem
from plone.app.contentmenu.interfaces import IWorkflowMenu
from plone.app.contentmenu.menu import BrowserSubMenuItem
from plone.app.contentmenu.menu import WorkflowMenu
from plone.protect.utils import addTokenToUrl
from Products.CMFCore.utils import getToolByName
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.security import checkPermission


@implementer(IActionsSubMenuItem)
class MyGroupSubMenuItem(BrowserSubMenuItem):
    title = 'Title of menu'
    submenuId = 'my_id'

    extra = {
        'id': 'plone-mymenuid',
        'li_class': 'plonetoolbar-myclass',
    }

    order = 70

    @property
    def action(self):
        return 'url-for-action'

    def available(self):
        if checkPermission('cmf.ModifyPortalContent', self.context):
            return True
        return False

    def selected(self):
        return False


@implementer(IWorkflowMenu)
class PKANWorkflowMenu(WorkflowMenu):

    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []

        locking_info = queryMultiAdapter((context, request),
                                         name='plone_lock_info')
        if locking_info and locking_info.is_locked_for_current_user():
            return []

        wf_tool = getToolByName(context, 'portal_workflow')

        workflowActions = wf_tool.listActionInfos(object=context)

        for action in workflowActions:
            if action['category'] != 'pkan_workflow':
                continue

            cssClass = ''
            actionUrl = action['url']
            if actionUrl == '':
                actionUrl = '{0}/content_status_modify?workflow_action={1}'
                actionUrl = actionUrl.format(
                    context.absolute_url(),
                    action['id'],
                )
                cssClass = ''

            description = ''

            transition = action.get('transition', None)
            if transition is not None:
                description = transition.description

            baseUrl = '{0}/content_status_modify?workflow_action={1}'
            for bogus in self.BOGUS_WORKFLOW_ACTIONS:
                if actionUrl.endswith(bogus):
                    if getattr(context, bogus, None) is None:
                        actionUrl = baseUrl.format(
                            context.absolute_url(),
                            action['id'],
                        )
                        cssClass = ''
                    break

            if action['allowed']:
                results.append({
                    'title': action['title'],
                    'description': description,
                    'action': addTokenToUrl(actionUrl, request),
                    'selected': False,
                    'icon': None,
                    'extra': {
                        'id': 'workflow-transition-{0}'.format(action['id']),
                        'separator': None,
                        'class': cssClass},
                    'submenu': None,
                })

        return results
