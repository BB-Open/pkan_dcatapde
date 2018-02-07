# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from pkan.dcatapde import constants
from pkan.dcatapde.harvesting.field_adapter.interfaces import IFieldProcessor
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import ComponentLookupError
from zope.component import getUtility
from zope.schema import getFieldsInOrder


# security related functions
def restore_user(old_sm):
    # restore security context of user
    if old_sm:
        setSecurityManager(old_sm)


def work_as_admin():
    """
    Analog to doing an "su root"
    :param request:
    :return:
    """
    current = api.user.get_current()
    old_sm = getSecurityManager()
    if current.id == 'admin':
        return old_sm
    # Save old user security context

    portal = api.portal.get()
    # start using as admin
    newSecurityManager(portal, portal.getOwner())
    return old_sm


# vocabulary related functions
def get_terms_for_ct(CT, prefix='', required=False):
    terms = []
    try:
        schema = getUtility(IDexterityFTI,
                            name=CT).lookupSchema()
    except ComponentLookupError:
        return terms
    fields = getFieldsInOrder(schema)
    for field_name, field in fields:
        adapter = IFieldProcessor(field)

        terms += adapter.get_terms_for_vocab(CT,
                                             field_name,
                                             prefix=prefix,
                                             required=required)

    return terms


# get functions
def get_parent(context):
    """
    get the parent return None if no parent is found
    """
    if context is None:
        return None

    aq_parent = getattr(context, 'aq_parent', None)

    if not aq_parent:
        uid = context.UID()
        context = api.content.get(UID=uid)
        if context is None:
            return None

    obj = context.aq_parent

    portal_type = getattr(obj, 'portal_type', None)

    if not portal_type:
        return None
    return obj


def get_ancestor(context, portal_type):
    """
    get a parent with the given type for the context where current user is
    return None if no parent is found
    """
    obj = context

    if not obj:
        return None

    old_portal_type = getattr(obj, 'portal_type', None)
    if not old_portal_type:
        return None

    while obj.portal_type != portal_type:
        obj = get_parent(obj)
        new_portal_type = getattr(obj, 'portal_type', None)
        if (not new_portal_type or
                (new_portal_type == constants.CT_PLONE_SITE) or
                not obj):
            return None

    return obj
