# -*- coding: utf-8 -*-
"""Post install import steps for pkan.dcatapde."""
from pkan.dcatapde import constants
from pkan.dcatapde.content.dcat_catalog import DCATCatalog
from pkan.dcatapde.content.dcat_dataset import DCATDataset
from pkan.dcatapde.content.dcat_distribution import DCATDistribution
from pkan.dcatapde.content.foaf_agent import FOAFAgent
from plone import api
from plone.app.dexterity.behaviors import constrains
from plone.indexer.interfaces import IIndexer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.ZCatalog.interfaces import IZCatalog
from zope.component import getGlobalSiteManager
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import Interface
from zope.interface.declarations import implementedBy
from zope.interface.declarations import Implements


@implementer(INonInstallable)
class HiddenProfiles(object):
    """Hidden GS profiles."""

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            'pkan.dcatapde:testfixture',
            'pkan.dcatapde:uninstall',
        ]


def pre_install(context):
    """Pre install script."""
    # Do something at the beginning of the installation of this package.


def post_install(context):
    """Post install script."""
    # Do something at the end of the installation of this package.
    portal = _get_navigation_root(context)
    add_default_folders(portal)
    set_constraints(context)


def post_install_testfixture(context):
    """Post install script for testfixture environments."""
    portal = _get_navigation_root(context)
    add_demo_content(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def add_default_folders(portal):
    """Add default folders on first install."""
    for folder_name, folder_type in constants.MANDATORY_FOLDERS.items():
        add_folder(portal, folder_name, folder_type)


def add_folder(portal_root, folder_name, folder_type):
    """Add a folder for the exclusive addition of certain CTs"""
    folder = portal_root.get(folder_name)
    if not folder:
        types = api.portal.get_tool(name='portal_types')
        fti = types.getTypeInfo(folder_type)
        fti.global_allow = True
        folder = api.content.create(
            container=portal_root,
            type=folder_type,
            id=folder_name,
            title=unicode(folder_name),
        )
        fti.global_allow = False
        _publish(folder)


def set_constraints(context):
    """Set content type constraints."""


def add_demo_content(portal):
    """Create some demo content."""


def _get_navigation_root(context):
    """Find the correct navigation root."""
    documents = api.content.find(portal_type='Document', id='front-page')
    if len(documents) == 0:
        return api.portal.get()
    front_page = documents[0].getObject()

    return api.portal.get_navigation_root(front_page)


def _publish(obj):
    """Publish the object if it hasn't been published."""
    if api.content.get_state(obj=obj) != 'published':
        api.content.transition(obj=obj, transition='publish')
        return True
    return False


def _setup_constrains(container, allowed_types):
    """Set allowed types as constraint for a given container."""
    behavior = ISelectableConstrainTypes(container)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setImmediatelyAddableTypes(allowed_types)
    return True


@implementer(IIndexer)
class DelegatingIndexer(object):
    """An indexer that delegates to a given callable."""

    def __init__(self, context, catalog, index_field):
        self.context = context
        self.catalog = catalog
        self.index_field = index_field

    def __call__(self):
        if not self.index_field:
            raise AttributeError
        return getattr(self.context, self.index_field)


class DelegatingIndexerFactory(object):
    """An adapter factory for an IIndexer.

    Works by calling a DelegatingIndexer.
    """

    def __init__(self, index_field):
        self.index_field = index_field
        self.__implemented__ = Implements(implementedBy(DelegatingIndexer))

    def __call__(self, object, catalog=None):
        return DelegatingIndexer(object, catalog, self.index_field)


def indexer_for_field_and_ct(field, ct):
    """Register a bad handler.

    Raises Attribute error for all other Instances.
    """
    gsm = getGlobalSiteManager()
    gsm.registerAdapter(
        factory=DelegatingIndexerFactory(None),
        required=(Interface, IZCatalog),
        name=field,
        provided=IIndexer,
    )

    """Register a good handler that returns the value of the field on
    the desired CT instances"""
    gsm = getGlobalSiteManager()
    gsm.registerAdapter(
        factory=DelegatingIndexerFactory(field),
        required=(ct, IZCatalog),
        name=field,
        provided=IIndexer,
    )


def catalog_setup(context):
    """Setup indices in the catalog."""
    # check if we are meant or called for other migration
    if context.readDataFile('pkan-various.txt') is None:
        # Not we self so exit
        return

    site = getSite()
    catalog = getToolByName(site, 'portal_catalog')
    # Get fields from the different models to build an index for
    content_type_extras = [
        DCATCatalog,
        DCATDataset,
        DCATDistribution,
        FOAFAgent,
    ]

    field_idxs = []
    # iterate over all content_type_extra classes
    for content_type_extra in content_type_extras:
        # collect the index_fields
        field_idxs += content_type_extra._index_fields
        """build IIndexer adapters to handle the indexing and prevent
        useless indexing by stopping aquisition from working on all
        other content_types
        """
        for field in content_type_extra._index_fields:
            indexer_for_field_and_ct(field, content_type_extra.content_schema)

    indexes = catalog.Indexes
    for name in field_idxs:
        if name not in indexes:
            catalog.addIndex(name, 'FieldIndex')
