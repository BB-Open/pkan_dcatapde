# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from plone.app.workflow import permissions
from plone.app.workflow.interfaces import ISharingPageRole
from plone.app.workflow.permissions import DelegateRoles
from zope.interface import implementer


@implementer(ISharingPageRole)
class PkanEditor(object):

    title = _(u'PkanEditor', default=u'PkanEditor')
    required_permission = DelegateRoles
    required_interface = None


@implementer(ISharingPageRole)
class CatalogAdmin(object):

    title = _(u'CatalogAdmin', default=u'CatalogAdmin')
    required_permission = permissions.DelegateEditorRole
    required_interface = None


@implementer(ISharingPageRole)
class CommuneEditor(object):

    title = _(u'CommuneEditor', default=u'CommuneEditor')
    required_permission = DelegateRoles
    required_interface = None
