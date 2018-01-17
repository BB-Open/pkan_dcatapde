# -*- coding: utf-8 -*-
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.interfaces import IJson
from pkan.dcatapde.harvesting.interfaces import IXml
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

    def read_fields(self):
        url = self.obj.url

        if not url:
            return []

        resp = requests.get(url=url)
        data = json.loads(resp.text)
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
