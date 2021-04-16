# -*- coding: utf-8 -*-
"""Upgrades."""
from AccessControl import Unauthorized
from Acquisition import aq_base
from Acquisition import aq_inner
from pkan.dcatapde.api.functions import get_parent
from pkan.dcatapde.browser.update_views.update_languages import UpdateLanguages
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import CT_DCAT_COLLECTION_CATALOG
from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.constants import CT_DCAT_DISTRIBUTION
from pkan.dcatapde.constants import CT_DCT_LANGUAGE
from pkan.dcatapde.constants import CT_DCT_LICENSEDOCUMENT
from pkan.dcatapde.constants import CT_DCT_LOCATION
from pkan.dcatapde.constants import CT_DCT_MEDIATYPEOREXTENT
from pkan.dcatapde.constants import CT_DCT_RIGHTSSTATEMENT
from pkan.dcatapde.constants import CT_DCT_STANDARD
from pkan.dcatapde.constants import CT_FOAF_AGENT
from pkan.dcatapde.constants import CT_HARVESTER
from pkan.dcatapde.constants import CT_HARVESTER_FOLDER
from pkan.dcatapde.constants import CT_RDFS_LITERAL
from pkan.dcatapde.constants import CT_SKOS_CONCEPT
from pkan.dcatapde.constants import CT_SKOS_CONCEPTSCHEME
from pkan.dcatapde.constants import CT_TRANSFER
from pkan.dcatapde.constants import DCAT_CTs
from pkan.dcatapde.constants import PROVIDER_ADMIN_ROLE
from pkan.dcatapde.constants import PROVIDER_CHIEF_EDITOR_ROLE
from pkan.dcatapde.constants import PROVIDER_DATA_EDITOR_ROLE
from pkan.dcatapde.content.base import add_obj_identifier
from pkan.dcatapde.harvesting.manager.interfaces import IRDFJSONLD
from pkan.dcatapde.harvesting.manager.interfaces import IRDFTTL
from pkan.dcatapde.harvesting.manager.interfaces import IRDFXML
from pkan.dcatapde.utils import get_available_languages_iso
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from plone.app.workflow.interfaces import ISharingPageRole
from plone.dexterity.factory import DexterityFactory
from plone.dexterity.interfaces import IDexterityFactory
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.interfaces import ISiteRoot
from ps.zope.i18nfield.field import I18NText
from ps.zope.i18nfield.field import I18NTextLine
from zope.component import getSiteManager
from zope.component import getUtility
from zope.component import IFactory
from zope.component import queryUtility
from zope.schema import getFields

import transaction


def update_role_mappings(context):
    wtool = api.portal.get_tool('portal_workflow')
    # copied from WorkflowTool.updateRoleMappings()
    # to enable context passing to wftool._recursiveUpdateRoleMappings()
    wfs = {}
    for id in wtool.objectIds():
        wf = wtool.getWorkflowById(id)
        if getattr(aq_base(wf), 'updateRoleMappingsFor', None):
            wfs[id] = wf
    context = aq_inner(context)
    wtool._recursiveUpdateRoleMappings(context, wfs)


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        'profile-pkan.dcatapde:default',
    )


def remove_defaultfactories(context):
    """
    Remove Custom DefaultFactories because they are not used.
    Add Dexterity DefaultFactory instead
    :param context:
    :return:
    """
    site = queryUtility(ISiteRoot)
    if site is None:
        return

    sm = getSiteManager(site)
    names = DCAT_CTs + [CT_HARVESTER, CT_HARVESTER_FOLDER]
    for name in names:

        sm.unregisterUtility(name=name, provided=IDexterityFactory)

        fti = getUtility(IDexterityFTI, name=name)

        factory_utility = queryUtility(IFactory, name=fti.factory)
        if factory_utility is None:
            sm.registerUtility(
                DexterityFactory(name),
                IFactory,
                fti.factory,
                info='plone.dexterity.dynamic',
            )
    transaction.commit()


def clean_value(field_value):
    new_value = {}
    for x in field_value.keys():
        lang = str(x)
        mess = field_value[x]
        available_languages_iso = get_available_languages_iso()
        if lang in available_languages_iso:
            new_value[available_languages_iso[lang]] = mess
    return new_value


def update_languages(context):
    reload_gs_profile(context)

    view = UpdateLanguages(context, getattr(context, 'REQUEST', None))
    view()

    transaction.commit()

    cts = [
        CT_DCAT_CATALOG,
        CT_DCAT_COLLECTION_CATALOG,
        CT_DCAT_DATASET,
        CT_DCAT_DISTRIBUTION,
        CT_DCT_LICENSEDOCUMENT,
        CT_DCT_LOCATION,
        CT_DCT_MEDIATYPEOREXTENT,
        CT_DCT_RIGHTSSTATEMENT,
        CT_DCT_STANDARD,
        CT_FOAF_AGENT,
        CT_SKOS_CONCEPTSCHEME,
        CT_RDFS_LITERAL,
        CT_SKOS_CONCEPT,
    ]

    portal = api.portal.get()
    if portal is None:
        return None

    changed_obj = []

    for ct in cts:
        results = api.content.find({'portal_type': ct})
        if not results:
            continue
        fti = getUtility(IDexterityFTI, name=ct)
        schema = fti.lookupSchema()
        fields = getFields(schema)

        for field_name in fields:
            field = fields[field_name]
            if isinstance(field, I18NText) or isinstance(field, I18NTextLine):
                for res in results:
                    obj = res.getObject()
                    field_value = getattr(obj, field_name, {})
                    if not field_value:
                        continue

                    new_value = clean_value(field_value)

                    if not new_value:
                        continue

                    setattr(obj, field_name, new_value)
                    if obj not in changed_obj:
                        changed_obj.append(obj)

    for obj in changed_obj:
        obj.reindexObject()
    transaction.commit()


def new_workflow(context):
    reload_gs_profile(context)

    portal = api.portal.get()
    if portal is None:
        return None
    results = api.content.find()
    for res in results:
        obj = res.getObject()
        update_role_mappings(obj)
        obj.reindexObjectSecurity()
        obj.reindexObject()

    transaction.commit()


def remove_role_utility(roles):
    site = queryUtility(ISiteRoot)
    if site is None:
        return

    sm = getSiteManager(site)
    for name in roles:
        sm.unregisterUtility(name=name, provided=ISharingPageRole)


def renamed_roles(context):
    reload_gs_profile(context)
    old_roles = {
        'PkanEditor': PROVIDER_DATA_EDITOR_ROLE,
        'CatalogAdmin': PROVIDER_CHIEF_EDITOR_ROLE,
        'CommuneEditor': PROVIDER_ADMIN_ROLE,
    }

    remove_role_utility(old_roles.keys())

    users = api.user.get_users()
    res = api.content.find(
        {'portal_type': [CT_DCAT_CATALOG, 'Folder']})

    for user in users:
        roles = api.user.get_roles(user=user)
        for role_name in old_roles.keys():
            if role_name in roles:
                roles.remove(role_name)
                roles.append(old_roles[role_name])
                api.user.grant_roles(user=user,
                                     roles=roles,
                                     )
        for brain in res:
            try:
                obj = brain.getObject()
            except Unauthorized:
                continue
            roles = api.user.get_roles(user=user,
                                       obj=obj)
            roles_parent = api.user.get_roles(user=user,
                                              obj=get_parent(obj))
            new_roles = []
            old_roles_to_remove = []
            for role_name in old_roles.keys():
                if role_name in roles and role_name not in roles_parent:
                    old_roles_to_remove.append(role_name)
                    new_roles.append(old_roles[role_name])
            if new_roles:
                api.user.grant_roles(user=user,
                                     roles=new_roles,
                                     obj=obj)
            if old_roles_to_remove:
                api.user.revoke_roles(user=user,
                                      roles=old_roles_to_remove,
                                      obj=obj)
            update_role_mappings(obj)
            obj.reindexObjectSecurity()
            obj.reindexObject()


def pkan_state(context):
    reload_gs_profile(context)
    new_workflow(context)


def update_uri_in_triplestore(context):
    """
    Updates skos concepts by setting their rdfs_isDefinedBy
    into uri_in_triplestore
    :param context:
    :return:
    """
    reload_gs_profile(context)

    cts = [
        CT_DCAT_CATALOG,
        CT_DCAT_COLLECTION_CATALOG,
        CT_DCAT_DATASET,
        CT_DCAT_DISTRIBUTION,
        CT_DCT_LICENSEDOCUMENT,
        CT_DCT_LOCATION,
        CT_DCT_MEDIATYPEOREXTENT,
        CT_DCT_RIGHTSSTATEMENT,
        CT_DCT_STANDARD,
        CT_FOAF_AGENT,
        CT_SKOS_CONCEPTSCHEME,
        CT_RDFS_LITERAL,
        CT_DCT_LANGUAGE,
        CT_SKOS_CONCEPT,
    ]

    for ct in cts:
        brains = api.content.find({'portal_type': ct})
        if not brains:
            continue
        for brain in brains:
            obj = brain.getObject()
            try:
                uri = obj.uri_in_triplestore
            except AttributeError:
                try:
                    uri = obj.rdfs_isDefinedBy
                except AttributeError:
                    continue
            obj.dct_identifier = uri

            obj.reindexObject()


def update_source_type(context):

    cts = [
        CT_HARVESTER,
        CT_TRANSFER,
    ]

    for ct in cts:
        brains = api.content.find(**{'portal_type': ct})
        if not brains:
            continue
        for brain in brains:
            obj = brain.getObject()
            type = str(obj.source_type)
            if 'IRDFXML' in type:
                obj.source_type = IRDFXML
            elif 'IRDFTTL' in type:
                obj.source_type = IRDFTTL
            elif 'IRDFJSON' in type:
                obj.source_type = IRDFJSONLD
            obj.reindexObject()


def update_identifier(context):
    cts = [
        CT_DCAT_CATALOG,
        CT_DCAT_COLLECTION_CATALOG,
        CT_DCAT_DATASET,
        CT_DCAT_DISTRIBUTION,
        CT_DCT_LICENSEDOCUMENT,
        CT_DCT_LOCATION,
        CT_DCT_MEDIATYPEOREXTENT,
        CT_DCT_RIGHTSSTATEMENT,
        CT_DCT_STANDARD,
        CT_FOAF_AGENT,
        CT_SKOS_CONCEPTSCHEME,
        CT_RDFS_LITERAL,
        CT_DCT_LANGUAGE,
        CT_SKOS_CONCEPT,
    ]

    for ct in cts:
        brains = api.content.find(**{'portal_type': ct})
        if not brains:
            continue
        for brain in brains:
            obj = brain.getObject()

            add_obj_identifier(obj, None)

            obj.reindexObject()


def update_transfer_enabled(context):
    cts = [CT_TRANSFER]

    for ct in cts:
        brains = api.content.find(**{'portal_type': ct})
        if not brains:
            continue
        for brain in brains:
            obj = brain.getObject()

            if obj.reharvesting_period:
                obj.is_enabled = True
            else:
                obj.is_enabled = False

            obj.reindexObject()
