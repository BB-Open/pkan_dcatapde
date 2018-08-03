# -*- coding: utf-8 -*-

# from plone import api
from Acquisition import aq_get
from pkan.dcatapde import _
from Products.CMFCore.utils import getToolByName
from Products.CMFDiffTool.utils import safe_unicode
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def get_states(wf):
    states_res = {}
    state_folder = getattr(wf, 'states', None)
    states = []
    if state_folder is not None:
        states = state_folder.values()

    for state in states:
        states_res[state.getId()] = {'title': state.title,
                                     'transitions': state.transitions}

    return states_res


@implementer(IVocabularyFactory)
class WorkflowStates(object):
    """
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        wf_name = 'simple_publication_workflow'
        start_state = 'private'

        site = getSite()
        wtool = getToolByName(site, 'portal_workflow', None)
        if wtool is None:
            return SimpleVocabulary([])

        wf = wtool.getWorkflowById(wf_name)
        # we get REQUEST from wtool because context may be an adapter
        request = aq_get(wtool, 'REQUEST', None)

        transitions = {}
        states = get_states(wf)

        transition_folder = getattr(wf, 'transitions', None)
        wf_name = wf.title or wf.id
        if transition_folder is not None:

            for transition in transition_folder.values():
                # zope.i18nmessageid will choke
                # if undecoded UTF-8 bytestrings slip through
                # which we may encounter on international sites
                # where transition names are in local language.
                # This may break overlying functionality even
                # if the terms themselves are never used
                name = safe_unicode(transition.actbox_name)
                new_state = transition.new_state_id

                transition_title = translate(
                    _(name),
                    context=aq_get(wtool, 'REQUEST', None))
                transitions[transition.id] = {'title': transition_title,
                                              'state': new_state}
        terms = []
        for t in states[start_state]['transitions']:
            t_info = transitions[t]
            t_state = t_info['state']
            t_state_title = translate(_(states[t_state]['title']),
                                      context=request)

            terms.append(
                SimpleTerm(t, title=u'{0} [{1}]'.format(
                    t_state_title,
                    t_state,
                )),
            )

        return SimpleVocabulary(terms)


WorkflowStatesFactory = WorkflowStates()
