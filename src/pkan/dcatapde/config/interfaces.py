# -*- coding: utf-8 -*-
"""Configuration Interfaces."""

from collective.z3cform.datagridfield import DictRow
from pkan.dcatapde import _
from pkan.dcatapde.api.harvester import get_all_harvester
from pkan.dcatapde.content.harvester import IHarvester
from plone.supermodel import model
from zope import schema


class HarvesterDefaultFactory(object):
    """Harvester Default Factory."""

    def __call__(self):
        harvester = get_all_harvester()
        res = []
        for harv in harvester:
            res.append({
                'title': harv.title,
                'url': harv.url,
                'harvesting_type': harv.harvesting_type,
                'data_cleaner': getattr(harv, 'data_cleaner', None),
                'source_type': harv.source_type,
            })
        return res


class IConfigHarvesterSchema(model.Schema):
    """Schema for Harvester Configuration."""

    harvester = schema.List(
        defaultFactory=HarvesterDefaultFactory(),
        description=_(u'Configure Harvester to be filled with exported Data'),
        required=False,
        title=_(u'Harvester'),
        value_type=DictRow(
            title=_(u'Tables'),
            schema=IHarvester,
        ),
    )
