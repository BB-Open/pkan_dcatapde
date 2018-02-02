# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from pkan.dcatapde.harvesting.field_adapter.interfaces import IFieldProcessor
from plone import api
# user related and security management methods
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import ComponentLookupError
from zope.component import getUtility
from zope.schema import getFields


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
    fields = getFields(schema)
    for field_name in fields.keys():
        field = fields[field_name]

        adapter = IFieldProcessor(field)

        terms += adapter.get_terms_for_vocab(CT,
                                             field_name,
                                             prefix=prefix,
                                             required=required)

    return terms
