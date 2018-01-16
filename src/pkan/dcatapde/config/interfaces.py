# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import DictRow
from pkan.dcatapde import _
from pkan.dcatapde.api.harvester import get_all_harvester
from pkan.dcatapde.content.harvester import IHarvester
from plone.supermodel import model
from zope import schema


class HarvesterDefaultFactory(object):
    def __call__(self):
        harvester = get_all_harvester()
        res = []
        for harv in harvester:
            res.append({
                'url': harv.url,
                'type': harv.type
            })
        return res


class IConfigHarvesterSchema(model.Schema):
    harvester = schema.List(
        title=_(u'Harvester'),
        description=_(
            u'''Configure Harvester to be filled with exported Data'''),
        defaultFactory=HarvesterDefaultFactory(),
        value_type=DictRow(
            title=_(u'Tables'),
            schema=IHarvester,
        ),
        required=False,
    )
