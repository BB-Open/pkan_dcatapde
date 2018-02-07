# -*- coding: utf-8 -*-
"""I18N message id's."""

from pkan.dcatapde import _
from pkan.dcatapde import constants


FIELDSET_RELATIONS = _(u'Relations')


HELP_DCT_HASPART = _(
    u'Link to an existing catalog or or create a new one by using the '
    u'\'add\' button below.',
)
HELP_DCT_ISPARTOF = _(
    u'Link to an existing parent catalog or or create a new one by using the '
    u'\'add\' button below.',
)
HELP_DCT_LICENSE = _(
    u'Select a license from the list of available licenses or create '
    u'a new one by using the \'add\' button below.',
)
HELP_DCT_PUBLISHER = _(
    u'Select a publisher from the list of available publishers or create '
    u'a new one by using the \'add\' button below.',
)
HELP_DCT_RIGHTS = _(
    u'Select a rights statement from the list of available statements or '
    u'create a new one by using the \'add\' button below.',
)
HELP_DCT_SPATIAL = _(
    u'Select a location from the list of available locations or '
    u'create a new one by using the \'add\' button below.',
)
HELP_DCT_THEMETAXONOMY = _(
    u'Select a theme taxonomy from the list of available taxonomies or '
    u'create a new one by using the \'add\' button below.',
)
HELP_FOLDER_AGENTS = _(
    u'Please enter the folder containing all agents, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_AGENTS),
    },
)
HELP_FOLDER_FORMATS = _(
    u'Please enter the folder containing all formats, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_FORMATS),
    },
)
HELP_FOLDER_LICENSES = _(
    u'Please enter the folder containing all licenses, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_LICENSES),
    },
)
HELP_FOLDER_LOCATIONS = _(
    u'Please enter the folder containing all locations, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_LOCATIONS),
    },
)
HELP_FOLDER_PUBLISHERS = _(
    u'Please enter the folder containing all publishers, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_PUBLISHERS),
    },
)
HELP_FOLDER_STANDARDS = _(
    u'Please enter the folder containing all standards, eg. ${folder}.',
    mapping={
        u'folder': u'/{0}'.format(constants.FOLDER_STANDARDS),
    },
)
HELP_SETTINGS_BASE = _(u'Manage base settings for PKAN.')
HELP_SETTINGS_FOLDERS = _(u'Manage folder settings for PKAN.')


LABEL_DCT_DESCRIPTION = _(u'Description')
LABEL_DCT_HASPART = _(u'Parts')
LABEL_DCT_ISPARTOF = _(u'Parent Catalog')
LABEL_DCT_ISSUED = _(u'Issued')
LABEL_DCT_LANGUAGE = _(u'Languages')
LABEL_DCT_LICENSE = _(u'License')
LABEL_DCT_MODIFIED = _(u'Modified')
LABEL_DCT_PUBLISHER = _(u'Publisher')
LABEL_DCT_RIGHTS = _(u'Rights')
LABEL_DCT_SPATIAL = _(u'Spatial relevance')
LABEL_DCT_THEMETAXONOMY = _(u'Theme Taxonomy')
LABEL_DCT_TITLE = _(u'Title')
LABEL_FOAF_HOMEPAGE = _(u'Homepage')
LABEL_FOLDER_AGENTS = _(u'Folder containing agents')
LABEL_FOLDER_FORMATS = _(u'Folder containing formats')
LABEL_FOLDER_LICENSES = _(u'Folder containing licenses')
LABEL_FOLDER_LOCATIONS = _(u'Folder containing locations')
LABEL_FOLDER_PUBLISHERS = _(u'Folder containing publishers')
LABEL_FOLDER_STANDARDS = _(u'Folder containing standards')
LABEL_SETTINGS_BASE = _(u'PKAN Base Settings')
LABEL_SETTINGS_FOLDERS = _(u'PKAN Folder Settings')


STATUS_REGISTRY_UPDATED = _(
    u'Registry has been updated. Please reload this page.',
)
