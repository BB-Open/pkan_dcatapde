# -*- coding: utf-8 -*-
"""Harvesting adapter."""
from pkan.dcatapde import constants as c
from pkan.dcatapde.api.catalog import add_catalog
from pkan.dcatapde.api.catalog import clean_catalog
from pkan.dcatapde.api.dataset import add_dataset
from pkan.dcatapde.api.dataset import clean_dataset
from pkan.dcatapde.api.distribution import add_distribution
from pkan.dcatapde.api.distribution import clean_distribution
from pkan.dcatapde.api.foafagent import add_foafagent
from pkan.dcatapde.api.foafagent import clean_foafagent
from pkan.dcatapde.api.harvester import get_field_config
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.field_adapter.interfaces import IFieldProcessor
from pkan.dcatapde.harvesting.interfaces import IJson
from pkan.dcatapde.harvesting.interfaces import IXml
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from z3c.relationfield import RelationChoice
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.schema import getFields

import json
import requests
import xml


ADD_METHODS_SUB_CTS = {
    c.CT_Foafagent: add_foafagent,
}

CLEAN_METHODS_SUB_CTS = {
    c.CT_Foafagent: clean_foafagent,
}


class BaseProcessor(object):
    """Base processor."""

    _schema_fields = {}

    def __init__(self, obj):
        self.obj = obj
        self.cleared_data = None
        self.field_config = get_field_config(self.obj)
        self.context = api.portal.get()
        if self.field_config:
            if self.field_config.base_object:
                self.context = self.field_config.base_object.to_object

    def get_schema_fields(self, ct):
        if ct in self._schema_fields:
            return self._schema_fields[ct]
        else:
            schema = getUtility(IDexterityFTI,
                                name=ct).lookupSchema()
            fields = getFields(schema)
            self._schema_fields[ct] = fields
            return fields

    def format_errors(self, errors, ct):
        formatted = ''
        for error in errors:
            error_name = error[1].__class__.__name__
            field_name = error[0]
            schema_fields = self.get_schema_fields(ct)
            field = schema_fields[field_name]
            if isinstance(field, RelationChoice):
                continue
            formatted += c.ERROR_HTML_LINE.format(
                error=error_name,
                field=field_name)
        return formatted

    def dry_run(self):  # noqa
        """Perform a dry run."""
        log = ''

        if not self.cleared_data:
            return '<p>No Data to Test</p>'

        keys = self.cleared_data.keys()

        pass_ct = []

        if self.context.portal_type == c.CT_Catalog:
            pass_ct.append(c.CT_Catalog)
        elif self.context.portal_type == c.CT_Dataset:
            pass_ct.append(c.CT_Catalog)
            pass_ct.append(c.CT_Dataset)
        elif self.context.portal_type == c.CT_Distribution:
            return log + '<p>Wrong context, cannot add anything</p>'

        if (
            c.CT_Catalog in self.cleared_data and
            self.cleared_data[c.CT_Catalog]
        ):
            catalogs = self.cleared_data[c.CT_Catalog]
            catalog_counter = len(catalogs)

            if c.CT_Catalog in pass_ct:
                for x in range(0, catalog_counter):
                    catalogs[x] = self.context
            else:
                for x in range(0, catalog_counter):
                    log += '<p>Start cleaning catalog number {catalog}</p>'.format(  # noqa
                        catalog=x,
                    )
                    if isinstance(catalogs[x], int):
                        pass
                    else:
                        # Fix: instead of create check for
                        # create/update/deprecated/delete
                        catalog, error = clean_catalog(**catalogs[x])
                        catalogs[x] = catalog
                        if error:
                            log += self.format_errors(error, c.CT_Catalog)
                    log += '<p>Cleaned catalog number {catalog}</p>'.format(
                        catalog=x)

        pass_dataset = c.CT_Dataset in pass_ct

        log += self.dry_run_for_type(
            c.CT_Dataset,
            c.CT_Catalog,
            clean_dataset,
            pass_obj=pass_dataset,
        )

        log += self.dry_run_for_type(
            c.CT_Distribution,
            c.CT_Dataset,
            clean_distribution,
        )

        for key in keys:
            key_elements = key.split(':')
            if len(key_elements) == 3 and key_elements[0] not in pass_ct:
                log += self.dry_run_for_subtype(key, key_elements)

        return log

    def real_run(self):
        """Create Objects.

        :return:
        """
        log = self.dry_run()

        if not self.cleared_data:
            return log + '<p>No data found, cannot add anything</p>'

        log += '<p>Doing Real Run<p>'

        keys = self.cleared_data.keys()

        pass_ct = self.get_content_to_pass()

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
                        # Fix: instead of create check for
                        # create/update/deprecated/delete
                        catalog = add_catalog(self.context, **catalogs[x])
                        catalogs[x] = catalog
                        log += '<p>Created catalog {catalog}</p>'.format(
                            catalog=catalog.title,
                        )

        pass_dataset = c.CT_Dataset in pass_ct

        log += self.real_run_for_type(
            c.CT_Dataset,
            c.CT_Catalog,
            add_dataset,
            pass_obj=pass_dataset,
        )

        log += self.real_run_for_type(
            c.CT_Distribution,
            c.CT_Dataset,
            add_distribution,
        )

        for key in keys:
            key_elements = key.split(':')

            if len(key_elements) >= 3 and key_elements[0] not in pass_ct:
                log += self.real_run_for_subtype(key, key_elements)

        for key in keys:
            key_elements = key.split(':')

            if len(key_elements) >= 3 and key_elements[0] not in pass_ct:
                log += self.set_subtypes_to_parent(key, key_elements)

        return log

    def real_run_for_subtype(self, key, key_elements):
        log = ''
        key_elements_length = len(key_elements)

        while key_elements_length >= 3:
            ct = key_elements[key_elements_length - 1]

            if ct in ADD_METHODS_SUB_CTS:
                add_routine = ADD_METHODS_SUB_CTS[ct]
            else:
                log = '<p>Could not create {key} '
                log += 'because of missing method.</p>'
                return log.format(key=key)

            data_elements = self.cleared_data[key]
            data_counter = len(data_elements)

            for x in range(0, data_counter):

                if isinstance(data_elements[x], int):
                    wanted_obj = data_elements[data_elements[x]]
                else:
                    # Fix: instead of create check for
                    # create/update/deprecated/delete
                    wanted_obj = add_routine(self.context, **data_elements[x])
                    data_elements[x] = wanted_obj
                    log += '<p>Created {ct} {dataset}</p>'.format(
                        ct=ct,
                        dataset=wanted_obj.title,
                    )

            key_elements_length -= 2

        return log

    def set_subtypes_to_parent(self, key, key_elements):
        log = ''
        key_elements_length = len(key_elements)

        while key_elements_length >= 3:
            parent_ct = ':'.join(key_elements[0:key_elements_length - 3])
            attr = key_elements[key_elements_length - 2]
            ct = key_elements[key_elements_length - 1]

            data_elements = self.cleared_data[key]
            data_counter = len(data_elements)

            for x in range(0, data_counter):
                if isinstance(data_elements[x], int):
                    wanted_obj = data_elements[data_elements[x]]
                else:
                    wanted_obj = data_elements[x]

                parent = self.cleared_data[parent_ct][x]
                if isinstance(parent, int):
                    parent = self.cleared_data[parent_ct][parent]

                # Fix: Check if this works with RelatedItem-Field
                setattr(parent, attr, wanted_obj)

                log += '<p>Added {ct} {dataset} to parent.</p>'.format(
                    ct=ct,
                    dataset=wanted_obj.title,
                )
            key_elements_length -= 2

    def real_run_for_type(
        self, obj_ct, parent_ct, add_routine, pass_obj=False,
    ):

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
                        # Fix: instead of create check for
                        # create/update/deprecated/delete
                        parent = self.cleared_data[parent_ct][x]
                        if isinstance(parent, int):
                            parent = self.cleared_data[parent_ct][parent]

                        dataset = add_routine(parent, **data_elements[x])
                        data_elements[x] = dataset
                        log += '<p>Created {ct} {dataset}</p>'.format(
                            ct=obj_ct,
                            dataset=dataset.title,
                        )

        return log

    def dry_run_for_type(
        self, obj_ct, parent_ct, clean_routine, pass_obj=False,
    ):

        log = ''

        if obj_ct in self.cleared_data and self.cleared_data[obj_ct]:
            data_elements = self.cleared_data[obj_ct]
            data_counter = len(data_elements)

            if pass_obj:
                for x in range(0, data_counter):
                    data_elements[x] = self.context
            else:
                for x in range(0, data_counter):
                    log += '<p>Start cleanig {ct} number {dataset}</p>'.format(
                        ct=obj_ct,
                        dataset=x,
                    )
                    if isinstance(data_elements[x], int):
                        pass
                    else:
                        dataset, error = clean_routine(**data_elements[x])
                        data_elements[x] = dataset

                        if error:
                            log += self.format_errors(error, obj_ct)
                    log += '<p>Cleaned {ct} number {dataset}</p>'.format(
                        ct=obj_ct,
                        dataset=x,
                    )

        return log

    def dry_run_for_subtype(self, key, key_elements):
        log = ''

        key_elements_length = len(key_elements)

        while key_elements_length >= 3:
            ct = key_elements[key_elements_length - 1]

            if ct in CLEAN_METHODS_SUB_CTS:
                clean_routine = CLEAN_METHODS_SUB_CTS[ct]
            else:
                log = '<p>Could not clean {key} because of missing method.</p>'
                return log.format(key=key)

            data_elements = self.cleared_data[key]
            data_counter = len(data_elements)

            for x in range(0, data_counter):
                log += '<p>Start cleaning {ct} number {dataset}</p>'.format(
                    ct=ct,
                    dataset=x,
                )
                if isinstance(data_elements[x], int):
                    pass
                else:

                    wanted_data, error = clean_routine(**data_elements[x])
                    data_elements[x] = wanted_data
                    if error:
                        log += self.format_errors(error, ct)
                log += '<p>Cleaned {ct} number {dataset}</p>'.format(
                    ct=ct,
                    dataset=x,
                )

            key_elements_length -= 2

        return log

    def get_content_to_pass(self):
        if self.context.portal_type == c.CT_Catalog:
            return [c.CT_Catalog]
        elif self.context.portal_type == c.CT_Dataset:
            return [c.CT_Catalog, c.CT_Dataset]
        elif self.context.portal_type == c.CT_Distribution:
            return [c.CT_Catalog, c.CT_Dataset, c.CT_Distribution]
        else:
            return []


@adapter(IHarvester)
@implementer(IJson)
class JsonProcessor(BaseProcessor):
    """JSON Processor."""

    def get_data(self):
        url = self.obj.url
        if not url:
            return []

        resp = requests.get(url=url)

        data = json.loads(resp.text)

        return data

    def read_fields(self, reread=False):
        if getattr(self.obj, 'fields', None) and not reread:
            return self.obj.fields

        data = self.get_data()
        fields = []

        data_to_process = [
            {
                'prefix': '',
                'subdata': data,
            },
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
                        'subdata': subdata[key],
                    })
            if isinstance(subdata, list):
                for element in subdata:
                    data_to_process.append({
                        'prefix': prefix,
                        'subdata': element,
                    })
            else:
                if prefix not in fields and prefix:
                    fields.append(prefix)

            data_to_process.remove(current_data)

        self.obj.fields = fields

        return fields

    def read_data(self):

        raw_data = self.read_raw_data()
        raw_data = self.clean_data_by_field(raw_data)
        data = self.clean_data(raw_data)

        return data

    def read_data_from_field(self, source_field, subdata):
        path = source_field.split('.')

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

    def read_raw_data(self):
        source_data = self.get_data()
        raw_data = {}
        for field_config in self.field_config.fields:
            dcat_field = field_config['dcat_field']
            source_field = field_config['source_field']
            prio = field_config['prio']

            if source_field:
                subdata = self.read_data_from_field(source_field, source_data)

                key = '{dcat_field}__{prio}'.format(
                    dcat_field=dcat_field,
                    prio=prio,
                )
                # Merge data with same prio
                if key in raw_data:
                    for element_index in range(len(subdata)):
                        try:
                            current_data = raw_data[key][element_index]
                        except IndexError:
                            raw_data[key].append(subdata[element_index])
                            continue
                        if isinstance(current_data, list):
                            current_data.append(subdata[element_index])
                        else:
                            raw_data[key][element_index] = [
                                current_data,
                                subdata[element_index],
                            ]
                # No data with same prio, so just use subdata
                else:
                    raw_data[key] = subdata

        return raw_data

    def clean_data(self, raw_data):
        data = {}
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
                    data[ct][x][attribute] = (field_data[x], field)
                    data_prio[ct][x][attribute] = prio
                else:
                    old_prio = data_prio[ct][x][attribute]
                    if old_prio < prio and field_data[x]:
                        data[ct][x][attribute] = (field_data[x], field)
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

    def clean_data_by_field(self, data):

        available_fields = data.keys()
        for field_id in available_fields:
            field_info = field_id.split('__')

            field_ct = field_info[0]
            if ':' in field_ct:
                field_ct = field_ct.split(':')[-1]
            field_name = field_info[1]
            schema_fields = self.get_schema_fields(field_ct)
            field = schema_fields[field_name]
            adapter = IFieldProcessor(field)

            data = adapter.clean_value(data, field_id)

        return data

    def dry_run(self):
        """Dry Run: Returns Log-Information.

        :return:
        """
        log = '<p>Doing a dry run</p>'

        data = self.read_data()
        self.cleared_data = self.obj.preprocessor(self).preprocess(data)

        log += super(JsonProcessor, self).dry_run()

        return log


@adapter(IHarvester)
@implementer(IXml)
class XmlProcessor(BaseProcessor):
    """XML Processor."""

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
                'subdata': et,
            },
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
                        'subdata': child,
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
        """Dry Run: Returns Log-Information.

        :return:
        """
