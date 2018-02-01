# -*- coding: utf-8 -*-
from collections import OrderedDict
from pkan.dcatapde import constants as c
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.harvesting_type.interfaces import IDefaultType
from pkan.dcatapde.harvesting.harvesting_type.interfaces import ILicenseType
from zope.component import adapter
from zope.interface import implementer


class BaseAdapter(object):

    def __init__(self, obj):
        self.obj = obj


@adapter(IHarvester)
@implementer(IDefaultType)
class DefaultType(BaseAdapter):

    def __init__(self, obj):
        self.obj = obj
        self.cts = OrderedDict()
        self.cts[c.CT_DCAT_CATALOG] = None
        self.cts[c.CT_DCAT_DATASET] = c.CT_DCAT_CATALOG
        self.cts[c.CT_DCAT_DISTRIBUTION] = c.CT_DCAT_DATASET

    def get_pass_cts(self, context):
        pass_ct = []
        if context.portal_type == c.CT_DCAT_CATALOG:
            pass_ct.append(c.CT_DCAT_CATALOG)
        elif context.portal_type == c.CT_DCAT_DATASET:
            pass_ct.append(c.CT_DCAT_CATALOG)
            pass_ct.append(c.CT_DCAT_DATASET)
        elif context.portal_type == c.CT_DCAT_DISTRIBUTION:
            pass_ct.append(c.CT_DCAT_CATALOG)
            pass_ct.append(c.CT_DCAT_DATASET)
            pass_ct.append(c.CT_DCAT_DISTRIBUTION)
        return pass_ct


@adapter(IHarvester)
@implementer(ILicenseType)
class LicenseType(BaseAdapter):

    def __init__(self, obj):
        self.obj = obj
        self.cts = OrderedDict()
        self.cts[c.CT_DCT_LICENSE_DOCUMENT] = None

    def get_pass_cts(self, context):
        return []
