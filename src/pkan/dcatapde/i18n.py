# -*- coding: utf-8 -*-
"""I18N message id's."""

from pkan.dcatapde import _
from pkan.dcatapde import constants


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
HELP_SETTINGS = _(u'Manage all PKAN specific settings.')


LABEL_FOLDER_AGENTS = _(u'Folder containing agents')
LABEL_FOLDER_FORMATS = _(u'Folder containing formats')
LABEL_FOLDER_LICENSES = _(u'Folder containing licenses')
LABEL_FOLDER_LOCATIONS = _(u'Folder containing locations')
LABEL_FOLDER_PUBLISHERS = _(u'Folder containing publishers')
LABEL_FOLDER_STANDARDS = _(u'Folder containing standards')
LABEL_SETTINGS = _(u'PKAN Settings')


STATUS_REGISTRY_UPDATED = _(
    u'Registry has been updated. Please reload this page.',
)
