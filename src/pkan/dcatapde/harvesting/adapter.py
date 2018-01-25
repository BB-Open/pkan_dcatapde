# -*- coding: utf-8 -*-
from pkan.dcatapde import constants as c
from pkan.dcatapde.api.catalog import add_catalog
from pkan.dcatapde.api.dataset import add_dataset
from pkan.dcatapde.api.distribution import add_distribution
from pkan.dcatapde.api.foafagent import add_foafagent
from pkan.dcatapde.api.harvester import get_field_config
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.interfaces import IJson
from pkan.dcatapde.harvesting.interfaces import IXml
from zope.component import adapter
from zope.interface import implementer

import json
import requests
import xml


ADD_METHODS_SUB_CTS = {
    c.CT_Foafagent: add_foafagent
}


class BaseProcessor(object):
    def __init__(self, obj):
        self.obj = obj
        self.cleared_data = None
        self.field_config = get_field_config(self.obj)
        self.context = self.field_config.base_object.to_object

    def dry_run(self):
        return ''

    def real_run(self):
        '''
        Create Objects
        :return:
        '''
        log = self.dry_run()

        if not self.cleared_data:
            return log + '<p>No data found, cannot add anything</p>'

        log += '<p>Doing Real Run<p>'

        keys = self.cleared_data.keys()

        pass_ct = []

        if self.context.portal_type == c.CT_Catalog:
            pass_ct.append(c.CT_Catalog)
        elif self.context.portal_type == c.CT_Dataset:
            pass_ct.append(c.CT_Catalog)
            pass_ct.append(c.CT_Dataset)
        elif self.context.portal_type == c.CT_Distribution:
            return log + '<p>Wrong context, cannot add anything</p>'

        if c.CT_Catalog in self.cleared_data and self.cleared_data[
                c.CT_Catalog]:
            catalogs = self.cleared_data[c.CT_Catalog]
            catalog_counter = len(catalogs)

            if c.CT_Catalog in pass_ct:
                for x in range(0, catalog_counter):
                    catalogs[x] = self.context
            else:
                for x in range(0, catalog_counter):
                    if isinstance(catalogs[x], int):
                        pass
                    else:
                        # TODO instead of create check for
                        # create/update/deprecated/delete
                        catalog = add_catalog(self.context, **catalogs[x])
                        catalogs[x] = catalog
                        log += '<p>Created catalog {catalog}</p>'.format(
                            catalog=catalog.title)

        pass_dataset = c.CT_Dataset in pass_ct

        log += self.real_run_for_type(c.CT_Dataset,
                                      c.CT_Catalog,
                                      add_dataset,
                                      pass_obj=pass_dataset)

        log += self.real_run_for_type(c.CT_Distribution,
                                      c.CT_Dataset,
                                      add_distribution)

        for key in keys:
            key_elements = key.split(':')
            if len(key_elements) == 3 and key_elements[0] not in pass_ct:
                log += self.real_run_for_subtype(key, key_elements)
                # TODO: What if RelatedItem of RelatedItem?
                # How deep do we have to go?

    def real_run_for_subtype(self, key, key_elements):
        log = ''
        parent_ct = key_elements[0]
        attr = key_elements[1]
        ct = key_elements[2]

        if ct in ADD_METHODS_SUB_CTS:
            add_routine = ADD_METHODS_SUB_CTS[ct]
        else:
            log = '<p>Could not create {key} because of missing method.</p>'
            return log.format(key=key)

        data_elements = self.cleared_data[key]
        data_counter = len(data_elements)

        for x in range(0, data_counter):

            if isinstance(data_elements[x], int):
                wanted_obj = data_elements[data_elements[x]]
            else:
                # TODO instead of create check for
                # create/update/deprecated/delete
                wanted_obj = add_routine(self.context, **data_elements[x])
                data_elements[x] = wanted_obj
                log += '<p>Created {ct} {dataset}</p>'.format(
                    ct=ct,
                    dataset=wanted_obj.title
                )

            parent = self.cleared_data[parent_ct][x]
            if isinstance(parent, int):
                parent = self.cleared_data[parent_ct][parent]

            # TODO: Check if this works with RelatedItem-Field
            setattr(parent, attr, wanted_obj)

    def real_run_for_type(self,
                          obj_ct,
                          parent_ct,
                          add_routine,
                          pass_obj=False):

        log = ''

        if obj_ct in self.cleared_data and self.cleared_data[obj_ct]:
            data_elements = self.cleared_data[obj_ct]
            data_counter = len(data_elements)

            if pass_obj:
                for x in range(0, data_counter):
                    data_elements[x] = self.context
            else:
                for x in range(0, data_counter):

                    if isinstance(data_elements[x], int):
                        pass
                    else:
                        # TODO instead of create check for
                        # create/update/deprecated/delete
                        parent = self.cleared_data[parent_ct][x]
                        if isinstance(parent, int):
                            parent = self.cleared_data[parent_ct][parent]

                        dataset = add_routine(parent, **data_elements[x])
                        data_elements[x] = dataset
                        log += '<p>Created {ct} {dataset}</p>'.format(
                            ct=obj_ct,
                            dataset=dataset.title
                        )

        return log


@adapter(IHarvester)
@implementer(IJson)
class JsonProcessor(BaseProcessor):
    def get_data(self):
        url = self.obj.url
        if not url:
            return []

        resp = requests.get(url=url)

        data = json.loads(resp.text)

        return data

    def read_fields(self, reread=False):
        if self.obj.fields and not reread:
            return self.obj.fields

        data = self.get_data()
        fields = []

        data_to_process = [
            {
                'prefix': '',
                'subdata': data
            }
        ]

        while data_to_process:
            current_data = data_to_process[0]
            prefix = current_data['prefix']
            subdata = current_data['subdata']
            if isinstance(subdata, dict):
                for key in subdata.keys():
                    if prefix:
                        new_prefix = prefix + '.' + key
                    else:
                        new_prefix = key
                    data_to_process.append({
                        'prefix': new_prefix,
                        'subdata': subdata[key]
                    })
            if isinstance(subdata, list):
                for element in subdata:
                    data_to_process.append({
                        'prefix': prefix,
                        'subdata': element
                    })
            else:
                if prefix not in fields and prefix:
                    fields.append(prefix)

            data_to_process.remove(current_data)

        self.obj.fields = fields

        return fields

    def read_data(self):
        source_data = self.get_data()
        data = {}

        raw_data = {}
        for field_config in self.field_config.fields:
            dcat_field = field_config['dcat_field']
            source_field = field_config['source_field']
            prio = field_config['prio']

            if source_field:
                path = source_field.split('.')

                subdata = source_data

                for x in path:
                    if isinstance(subdata, dict):
                        subdata = subdata[x]
                    elif isinstance(subdata, list):
                        new_subdata = []
                        for sd in subdata:
                            if sd and x in sd:
                                new_subdata.append(sd[x])
                            else:
                                new_subdata.append(None)
                        subdata = new_subdata

                key = '{dcat_field}__{prio}'.format(dcat_field=dcat_field,
                                                    prio=prio)
                raw_data[key] = subdata

        data_prio = {}

        for field in raw_data:
            field_path = field.split('__')
            ct = field_path[0]
            attribute = field_path[1]
            prio = int(field_path[-1])

            field_data = raw_data[field]

            if ct not in data:
                data[ct] = {}
                data_prio[ct] = {}

            for x in range(len(field_data)):
                if x not in data[ct]:
                    data[ct][x] = {}
                    data_prio[ct][x] = {}
                if attribute not in data[ct][x]:
                    data[ct][x][attribute] = field_data[x]
                    data_prio[ct][x][attribute] = prio
                else:
                    old_prio = data_prio[ct][x][attribute]
                    if old_prio < prio and field_data[x]:
                        data[ct][x][attribute] = field_data[x]
                        data_prio[ct][x][attribute] = prio

        # find duplicates, because they are pointing the same object
        for ct in data:
            ct_data = {}
            for x in range(len(data[ct].keys())):
                data_str = str(data[ct][x])
                if data_str in ct_data:
                    data[ct][x] = ct_data[data_str]
                else:
                    ct_data[data_str] = x

        return data

    def dry_run(self):
        '''
        Dry Run: Returns Log-Information
        :return:
        '''

        log = '<p>Doing a dry run</p>'

        data = self.read_data()
        self.cleared_data = self.obj.preprocessor(self).preprocess(data)

        log += '<p>Data found:</p>'
        log += '<p>' + str(self.cleared_data) + '</p>'

        return log


@adapter(IHarvester)
@implementer(IXml)
class XmlProcessor(BaseProcessor):
    def read_fields(self, reread=False):
        if self.obj.fields and not reread:
            return self.obj.fields

        url = self.obj.url

        if not url:
            return []

        resp = requests.get(url=url)
        data = resp.text

        et = xml.etree.ElementTree.fromstring(data)

        fields = []

        data_to_process = [
            {
                'prefix': self.format_tag(et.tag),
                'subdata': et
            }
        ]

        while data_to_process:
            current_data = data_to_process[0]
            prefix = current_data['prefix']
            subdata = current_data['subdata']
            if subdata._children:
                for child in subdata:
                    if prefix:
                        new_prefix = prefix + '.' + self.format_tag(child.tag)
                    else:
                        new_prefix = self.format_tag(child.tag)
                    data_to_process.append({
                        'prefix': new_prefix,
                        'subdata': child
                    })
            else:
                if prefix not in fields and prefix:
                    fields.append(prefix)

            data_to_process.remove(current_data)

        self.obj.fields = fields

        return fields

    def format_tag(self, tag):
        return tag.split('}')[-1]

    def dry_run(self):
        '''
        Dry Run: Returns Log-Information
        :return:
        '''
