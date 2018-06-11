# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from pkan.dcatapde import _
from plone.app.contentmenu.interfaces import IActionsSubMenuItem
from plone.app.contentmenu.interfaces import IWorkflowMenu
from plone.app.contentmenu.menu import BrowserSubMenuItem
from plone.app.contentmenu.menu import WorkflowMenu
from plone.app.contentmenu.menu import WorkflowSubMenuItem
from plone.memoize.instance import memoize
from plone.protect.utils import addTokenToUrl
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface import implementer


@implementer(IActionsSubMenuItem)
class PKANSubMenuItem(WorkflowSubMenuItem):
    title = _(u'PKAN Object Status')
    submenuId = 'pkan_activation'
    short_title = _(u'State')

    order = 21

    def __init__(self, context, request):
        BrowserSubMenuItem.__init__(self, context, request)
        self.tools = getMultiAdapter((context, request), name='plone_tools')
        self.context = context

    @property
    def extra(self):
        tool = getToolByName(self.context, 'portal_workflow')
        state = tool.getInfoFor(aq_inner(self.context), 'pkan_state', None)
        stateTitle = self._currentStateTitle()
        return {'id': 'plone-contentmenu-workflow',
                'class': 'state-{0}'.format(state),
                'state': state,
                'stateTitle': stateTitle,
                'shortTitle': self.short_title,
                'li_class': 'plonetoolbar-workfow-transition'}

    @memoize
    def available(self):
        tool = getToolByName(self.context, 'portal_workflow')
        state = tool.getInfoFor(aq_inner(self.context), 'pkan_state', None)
        return (state is not None)

    @memoize
    def _currentStateTitle(self):
        tool = getToolByName(self.context, 'portal_workflow')
        state = tool.getInfoFor(aq_inner(self.context), 'pkan_state', None)
        workflows = self.tools.workflow().getWorkflowsFor(self.context)
        if workflows:
            for w in workflows:
                if state in w.states:
                    return w.states[state].title or state


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
