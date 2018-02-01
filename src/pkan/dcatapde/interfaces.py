# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from pkan.dcatapde import _
from pkan.dcatapde import constants
from plone.supermodel import model
from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IPkanDcatapdeLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPKANSettings(model.Schema):
    """PKAN settings."""

    folder_agents = schema.TextLine(
        default=u'/{0}'.format(constants.FOLDER_AGENTS),
        required=True,
        title=_(u'Folder containing agents'),
    )

    folder_formats = schema.TextLine(
        default=u'/{0}'.format(constants.FOLDER_FORMATS),
        required=True,
        title=_(u'Folder containing formats'),
    )

    folder_licenses = schema.TextLine(
        default=u'/{0}'.format(constants.FOLDER_LICENSES),
        required=True,
        title=_(u'Folder containing licenses'),
    )

    folder_locations = schema.TextLine(
        default=u'/{0}'.format(constants.FOLDER_LOCATIONS),
        required=True,
        title=_(u'Folder containing locations'),
    )

    folder_publishers = schema.TextLine(
        default=u'/{0}'.format(constants.FOLDER_PUBLISHERS),
        required=True,
        title=_(u'Folder containing publishers'),
    )

    folder_standards = schema.TextLine(
        default=u'/{0}'.format(constants.FOLDER_STANDARDS),
        required=True,
        title=_(u'Folder containing standards'),
    )
