# -*- coding: utf-8 -*-
"""Upgrades."""
from pkan.dcatapde.browser.update_views.update_languages import UpdateLanguages
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import CT_DCAT_COLLECTION_CATALOG
from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.constants import CT_DCAT_DISTRIBUTION
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
from pkan.dcatapde.constants import DCAT_CTs
from pkan.dcatapde.utils import get_available_languages_iso
from plone.app.upgrade.utils import loadMigrationProfile
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
from zope.component.hooks import getSite
from zope.schema import getFields

import transaction


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
        lang = unicode(x)
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

    portal = getSite()
    if portal is None:
        return None
    catalog = portal.portal_catalog

    changed_obj = []

    for ct in cts:
        results = catalog.searchResults({'portal_type': ct})
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
