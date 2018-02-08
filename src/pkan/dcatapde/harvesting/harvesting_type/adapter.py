# -*- coding: utf-8 -*-
from collections import OrderedDict
from pkan.dcatapde import constants as c
from pkan.dcatapde.api.harvester_field_config import get_field_config
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.harvesting_type.interfaces import IDefaultType
from pkan.dcatapde.harvesting.harvesting_type.interfaces import ILicenseType
from zope.component import adapter
from zope.interface import implementer


class BaseAdapter(object):

    def __init__(self, obj):
        self.obj = obj
        self.cts = OrderedDict

    def get_used_cts(self):
        context = None
        if self.obj:
            field_config = get_field_config(self.obj)
            if field_config:
                context = getattr(field_config, 'base_object', None)
                if context:
                    # fix: check why sometime to_object and sometimes not
                    context = getattr(context,
                                      'to_object',
                                      context)

        pass_ct = self.get_pass_cts(context)

        cts = list(set(self.cts.keys()) - set(pass_ct))
        return cts


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
        if not context:
            return pass_ct
        elif context.portal_type == c.CT_DCAT_CATALOG:
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
