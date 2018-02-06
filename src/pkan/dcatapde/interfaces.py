# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from pkan.dcatapde import constants
from pkan.dcatapde import i18n
from plone.supermodel import model
from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IPkanDcatapdeLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPKANBaseSettings(model.Schema):
    """PKAN Base Settings."""


class IPKANFolderSettings(model.Schema):
    """PKAN Folder Settings."""

    folder_agents = schema.TextLine(
        default=u'/{0}'.format(constants.FOLDER_AGENTS),
        description=i18n.HELP_FOLDER_AGENTS,
        required=True,
        title=i18n.LABEL_FOLDER_AGENTS,
    )

    folder_formats = schema.TextLine(
        default=u'/{0}'.format(constants.FOLDER_FORMATS),
        description=i18n.HELP_FOLDER_FORMATS,
        required=True,
        title=i18n.LABEL_FOLDER_FORMATS,
    )

    folder_licenses = schema.TextLine(
        default=u'/{0}'.format(constants.FOLDER_LICENSES),
        description=i18n.HELP_FOLDER_LICENSES,
        required=True,
        title=i18n.LABEL_FOLDER_LICENSES,
    )

    folder_locations = schema.TextLine(
        default=u'/{0}'.format(constants.FOLDER_LOCATIONS),
        description=i18n.HELP_FOLDER_LOCATIONS,
        required=True,
        title=i18n.LABEL_FOLDER_LOCATIONS,
    )

    folder_publishers = schema.TextLine(
        default=u'/{0}'.format(constants.FOLDER_PUBLISHERS),
        description=i18n.HELP_FOLDER_PUBLISHERS,
        required=True,
        title=i18n.LABEL_FOLDER_PUBLISHERS,
    )

    folder_standards = schema.TextLine(
        default=u'/{0}'.format(constants.FOLDER_STANDARDS),
        description=i18n.HELP_FOLDER_STANDARDS,
        required=True,
        title=i18n.LABEL_FOLDER_STANDARDS,
    )
