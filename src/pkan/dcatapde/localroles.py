# -*- coding: utf-8 -*-
from plone.app.workflow import permissions
from plone.app.workflow.interfaces import ISharingPageRole
from plone.app.workflow.permissions import DelegateRoles
from zope.interface import implementer

from pkan.dcatapde import _


@implementer(ISharingPageRole)
class ProviderDataEditor(object):

    title = _(u'ProviderDataEditor', default=u'ProviderDataEditor')
    required_permission = DelegateRoles
    required_interface = None


@implementer(ISharingPageRole)
class ProviderChiefEditor(object):

    title = _(u'ProviderChiefEditor', default=u'ProviderChiefEditor')
    required_permission = permissions.DelegateEditorRole
    required_interface = None


@implementer(ISharingPageRole)
class ProviderAdmin(object):

    title = _(u'ProviderAdmin', default=u'ProviderAdmin')
    required_permission = DelegateRoles
    required_interface = None
