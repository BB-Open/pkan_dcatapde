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
    states = []
    state_folder = getattr(wf, 'states', None)
    if state_folder is not None:
        states = state_folder.values()

    return [(s.title, s.getId()) for s in states]


@implementer(IVocabularyFactory)
class WorkflowStates(object):
    """
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        site = getSite()
        wtool = getToolByName(site, 'portal_workflow', None)
        if wtool is None:
            return SimpleVocabulary([])

        # we get REQUEST from wtool because context may be an adapter
        request = aq_get(wtool, 'REQUEST', None)

        wf = wtool.getWorkflowById('simple_publication_workflow')

        items = get_states(wf)
        items = [(safe_unicode(i[0]), i[1]) for i in items]
        items_dict = dict(  # no dict comprehension in py 2.6
            [
                (i[1], translate(_(i[0]), context=request))
                for i in items
            ],
        )
        items_list = [(k, v) for k, v in items_dict.items()]
        items_list.sort(lambda x, y: cmp(x[1], y[1]))
        terms = [
            SimpleTerm(k, title=u'{0} [{1}]'.format(v, k))
            for k, v in items_list
        ]

        return SimpleVocabulary(terms)


WorkflowStatesFactory = WorkflowStates()
