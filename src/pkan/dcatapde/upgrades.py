# -*- coding: utf-8 -*-
"""Upgrades."""

from pkan.dcatapde.constants import CT_HARVESTER
from pkan.dcatapde.constants import CT_HARVESTER_FOLDER
from pkan.dcatapde.constants import DCAT_CTs
from plone.app.upgrade.utils import loadMigrationProfile
from plone.dexterity.factory import DexterityFactory
from plone.dexterity.interfaces import IDexterityFactory
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getGlobalSiteManager
from zope.component import getUtility
from zope.component import IFactory
from zope.component import queryUtility


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
    gsm = getGlobalSiteManager()
    names = DCAT_CTs + [CT_HARVESTER, CT_HARVESTER_FOLDER]
    for name in names:
        gsm.unregisterUtility(name=name, provided=IDexterityFactory)

        fti = getUtility(IDexterityFTI, name=name)

        factory_utility = queryUtility(IFactory, name=fti.factory)
        if factory_utility is None:
            gsm.registerUtility(
                DexterityFactory(name),
                IFactory,
                fti.factory,
                info='plone.dexterity.dynamic',
            )
