# -*- coding: utf-8 -*-
from pkan.dcatapde.api.harvester import get_field_config
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.interfaces import IJson
from pkan.dcatapde.harvesting.interfaces import IXml
from pkan.dcatapde.harvesting.prep_interfaces import IPreprocessor
from zope.component import adapter
from zope.interface import implementer

import json
import requests
import xml


@adapter(IHarvester)
@implementer(IJson)
class JsonProcessor(object):

    def __init__(self, obj):
        self.obj = obj
        self.cleared_data = None
        self.field_config = get_field_config(self.obj)

    def get_data(self):
        url = self.obj.url

        if not url:
            return []

        resp = requests.get(url=url)
        data = json.loads(resp.text)
        return data

    def read_fields(self):
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

        return fields

    def read_data(self):
        source_data = self.get_data()
        data = {}

        raw_data = {}
        for field_config in self.field_config.fields:
            dcat_field = field_config['dcat_field']
            source_field = field_config['source_field']

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

                raw_data[dcat_field] = subdata

        for field in raw_data:
            field_path = field.split('__')
            ct = field_path[0]
            attribute = field_path[1]

            field_data = raw_data[field]

            if ct not in data:
                data[ct] = {}

            for x in range(len(field_data)):
                if x not in data[ct]:
                    data[ct][x] = {}
                data[ct][x][attribute] = field_data[x]

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
        self.cleared_data = IPreprocessor(self).preprocess(data)

        log += '<p>Data found:</p>'
        log += '<p>' + str(self.cleared_data) + '</p>'

        return log

    def real_run(self):
        '''
        Create Objects
        :return:
        '''

        if not self.cleared_data:
            self.dry_run()


@adapter(IHarvester)
@implementer(IXml)
class XmlProcessor(object):

    def __init__(self, obj):
        self.obj = obj

    def read_fields(self):
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

        return fields

    def format_tag(self, tag):
        return tag.split('}')[-1]

    def dry_run(self):
        '''
        Dry Run: Returns Log-Information
        :return:
        '''

    def real_run(self):
        '''
        Create Objects
        :return:
        '''
