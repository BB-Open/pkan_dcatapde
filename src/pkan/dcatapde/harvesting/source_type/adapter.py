# -*- coding: utf-8 -*-
"""Harvesting adapter."""
from pkan.dcatapde import constants as c
from pkan.dcatapde.api.dcat_catalog import add_catalog
from pkan.dcatapde.api.dcat_catalog import clean_catalog
from pkan.dcatapde.api.dcat_dataset import add_dataset
from pkan.dcatapde.api.dcat_dataset import clean_dataset
from pkan.dcatapde.api.dcat_distribution import add_distribution
from pkan.dcatapde.api.dcat_distribution import clean_distribution
from pkan.dcatapde.api.dct_licensedocument import add_dct_licensedocument
from pkan.dcatapde.api.dct_licensedocument import clean_dct_licensedocument
from pkan.dcatapde.api.foaf_agent import add_foafagent
from pkan.dcatapde.api.foaf_agent import clean_foafagent
from pkan.dcatapde.api.functions import get_terms_for_ct
from pkan.dcatapde.api.harvester_field_config import get_field_config
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.field_adapter.interfaces import IFieldProcessor
from pkan.dcatapde.harvesting.source_type.data import DataManager
from pkan.dcatapde.harvesting.source_type.interfaces import IJson
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from z3c.relationfield import RelationChoice
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.schema import Choice
from zope.schema import getFields

import json
import urllib


# FIX: Fill with all Cts
ADD_METHODS_CTS = {
    c.CT_FOAF_AGENT: add_foafagent,
    c.CT_DCAT_DATASET: add_dataset,
    c.CT_DCAT_DISTRIBUTION: add_distribution,
    c.CT_DCAT_CATALOG: add_catalog,
    c.CT_DCT_LICENSEDOCUMENT: add_dct_licensedocument,
}

CLEAN_METHODS_CTS = {
    c.CT_FOAF_AGENT: clean_foafagent,
    c.CT_DCAT_CATALOG: clean_catalog,
    c.CT_DCAT_DATASET: clean_dataset,
    c.CT_DCAT_DISTRIBUTION: clean_distribution,
    c.CT_DCT_LICENSEDOCUMENT: clean_dct_licensedocument,
}


class BaseProcessor(object):
    # helper

    _schema_fields = {}

    def __init__(self, harvester):
        self.harvester = harvester
        self.harvesting_type = self.harvester.harvesting_type(self.harvester)
        self.data_type = self.harvester.data_type(self.harvester)
        self.cleaned_data = None
        self.field_config = get_field_config(self.harvester)
        self.context = api.portal.get()
        if self.field_config:
            if self.field_config.base_object:
                # fix: check why sometime to_object and sometimes not
                self.context = getattr(self.field_config.base_object,
                                       'to_object',
                                       self.field_config.base_object)

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
            elif isinstance(field, Choice):
                proc = IFieldProcessor(field)
                if proc.get_cts_from_relfield(field, field_name):
                    continue
            if (not field.required and
                    error_name == 'SchemaNotFullyImplemented'):
                continue
            formatted += c.ERROR_HTML_LINE.format(
                error=error_name,
                field=field_name)
        return formatted

    def read_available_fields(self):
        """Read fields from data source.

        :return: list of fields
        """
        return []

    def read_dcat_fields(self, ct=None):
        """
        Read fields for dcat plone objects
        :return: Terms for vocabulary
        """
        terms = []

        # if a ct is given, we just want to use th
        if ct is not None:
            return get_terms_for_ct(ct)
        for ct in self.harvesting_type.get_used_cts():
            terms += get_terms_for_ct(ct)
        return terms

    def read_values(self):
        """Read field values from source url
        Result must be data dict like
        {ct_identifier: {index: {field: list of data}}}

        :return:
        """
        self.cleaned_data = None

    def clean_data(self):
        """
        Clean data in multiple steps:
         1. data_type cleaning
         2. data config cleaning
         3. finding duplicates
        Result must be data-dict like
        {ct_identifier: {index: {field: list of data}}}
        :return:
        """
        if self.cleaned_data:
            self.data_type.clean_data(self.cleaned_data)
            self.clean_data_by_config(self.cleaned_data)
            self.clean_duplicate(self.cleaned_data)

    def clean_data_by_field(self, data):
        """

        :param data: dict like {field_identifier: list of values}
        :return: dict like {field_identifier: list of values}
        """

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

    def clean_duplicate(self, data_manager):
        data_manager.clean_duplicates()

    def clean_data_by_config(self, cleaned_data):
        pass

    def dry_run(self):
        """Dry Run: Returns Log-Information.

        :return: log information
        """
        self.read_values()
        self.clean_data()

        log = ''

        if not self.cleaned_data:
            return '<p>No Data to Test</p>'

        cts = self.cleaned_data.cts

        pass_ct = self.harvesting_type.get_pass_cts(self.context)

        # FIX: all CT-Information should not be written here

        for ct in self.harvesting_type.cts.keys():
            pass_obj = ct in pass_ct

            log += self.dry_run_for_type(
                ct,
                pass_obj=pass_obj,
            )

        for key in cts:
            key_elements = key.split(':')
            if len(key_elements) == 3 and key_elements[0] not in pass_ct:
                log += self.dry_run_for_subtype(key, key_elements)

        return log

    def real_run(self):
        """Create Objects.

        :return: log information
        """

        log = self.dry_run()

        if not self.cleaned_data.data:
            return log + '<p>No data found, cannot add anything</p>'

        log += '<p>Doing Real Run<p>'

        cts = self.cleaned_data.cts

        pass_ct = self.harvesting_type.get_pass_cts(self.context)

        for ct in self.harvesting_type.cts.keys():
            pass_obj = ct in pass_ct

            log += self.real_run_for_type(
                ct,
                self.harvesting_type.cts[ct],
                pass_obj=pass_obj,
            )

        for key in cts:
            key_elements = key.split(':')

            if len(key_elements) >= 3 and key_elements[0] not in pass_ct:
                log += self.real_run_for_subtype(key, key_elements)

        for key in cts:
            key_elements = key.split(':')

            if len(key_elements) >= 3 and key_elements[0] not in pass_ct:
                log += self.set_subtypes_to_parent(key, key_elements)

        return log

    def real_run_for_subtype(self, key, key_elements):
        log = ''
        key_elements_length = len(key_elements)

        while key_elements_length >= 3:
            ct = key_elements[key_elements_length - 1]

            if ct in ADD_METHODS_CTS:
                add_routine = ADD_METHODS_CTS[ct]
            else:
                log = '<p>Could not create {key} '
                log += 'because of missing method.</p>'
                return log.format(key=key)

            data_elements = self.cleaned_data.get_data_for_ct(key)

            for id in data_elements:
                # Fix: instead of create check for
                # create/update/deprecated/delete
                wanted_obj = add_routine(self.context, **data_elements[id])
                self.cleaned_data.set_created_obj(key, id, wanted_obj)
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
            parent_ct = ':'.join(key_elements[0:key_elements_length - 2])
            attr = key_elements[key_elements_length - 2]
            ct = key_elements[key_elements_length - 1]

            current_key = ':'.join([parent_ct, attr, ct])

            data_elements = self.cleaned_data.get_all_created(current_key)

            for id in data_elements:

                wanted_obj = data_elements[id]

                parent = self.cleaned_data.get_created(parent_ct, id)
                if not parent:
                    log += '<p>Could not link {ct} {dataset}.</p>'.format(
                        ct=ct,
                        dataset=wanted_obj.title,
                    )
                    continue

                # Fix: Check if this works with RelatedItem-Field
                setattr(parent, attr, wanted_obj.UID())

                log += '<p>Added {ct} {dataset} to parent.</p>'.format(
                    ct=ct,
                    dataset=wanted_obj.title,
                )
            key_elements_length -= 2
        return log

    def real_run_for_type(
        self, obj_ct, parent_ct, pass_obj=False,
    ):

        log = ''

        if obj_ct in ADD_METHODS_CTS:
            add_routine = ADD_METHODS_CTS[obj_ct]
        else:
            log = '<p>Could not create {key} '
            log += 'because of missing method.</p>'
            return log.format(key=obj_ct)

        data = self.cleaned_data.get_data_for_ct(obj_ct)

        if not data:
            return '<p>Nothing to check for {ct}</p>'.format(ct=obj_ct)

        for id in data:
            if pass_obj:
                self.cleaned_data.set_created_obj(obj_ct, id, None)
            else:
                log += '<p>Start cleanig {ct} number {dataset}</p>'.format(
                    ct=obj_ct,
                    dataset=id,
                )

                parent = None

                # if no parent_ct is given, use given context
                if not parent_ct:
                    parent = self.context
                # if parent_ct is given and the context has the same type
                # use context
                if self.context.portal_type == parent_ct:
                    parent = self.context
                # if parent_ct is given, but context has different type
                # we need a created object as context
                elif parent_ct:
                    parent = self.cleaned_data.get_created(parent_ct, id)

                if not parent:
                    log += """<p>Could not create {ct} {dataset}.
                        No context</p>""".format(
                        ct=obj_ct,
                        dataset=id,
                    )
                    continue

                # Fix: instead of create check for
                # create/update/deprecated/delete
                dataset = add_routine(parent, **data[id])
                self.cleaned_data.set_created_obj(obj_ct, id, dataset)

                log += '<p>Created {ct} {dataset}</p>'.format(
                    ct=obj_ct,
                    dataset=dataset.title,
                )

        return log

    def dry_run_for_type(
        self, obj_ct, pass_obj=False,
    ):

        log = ''

        if obj_ct in CLEAN_METHODS_CTS:
            clean_routine = CLEAN_METHODS_CTS[obj_ct]
        else:
            return '<p>No clean method for {ct}</p>'.format(ct=obj_ct)

        data = self.cleaned_data.get_data_for_ct(obj_ct)

        if not data:
            return '<p>Nothing to check for {ct}</p>'.format(ct=obj_ct)

        for id in data:
            if pass_obj:
                self.cleaned_data.set_created_obj(obj_ct, id, None)
            else:
                log += '<p>Start cleanig {ct} number {dataset}</p>'.format(
                    ct=obj_ct,
                    dataset=id,
                )
                dataset, error = clean_routine(**data[id])
                self.cleaned_data.update(obj_ct, id, dataset)
                if error:
                    log += self.format_errors(error, obj_ct)
                log += '<p>Cleaned {ct} number {dataset}</p>'.format(
                    ct=obj_ct,
                    dataset=id,
                )

        return log

    def dry_run_for_subtype(self, key, key_elements):
        log = ''

        key_elements_length = len(key_elements)

        while key_elements_length >= 3:
            ct = key_elements[key_elements_length - 1]

            if ct in CLEAN_METHODS_CTS:
                clean_routine = CLEAN_METHODS_CTS[ct]
            else:
                log = '<p>Could not clean {key} because of missing method.</p>'
                return log.format(key=key)

            data_elements = self.cleaned_data.get_data_for_ct(key)

            for id in data_elements:
                log += '<p>Start cleaning {ct} number {dataset}</p>'.format(
                    ct=ct,
                    dataset=id,
                )
                wanted_data, error = clean_routine(**data_elements[id])
                self.cleaned_data.update(key, id, wanted_data)
                if error:
                    log += self.format_errors(error, ct)
                log += '<p>Cleaned {ct} number {dataset}</p>'.format(
                    ct=ct,
                    dataset=id,
                )

            key_elements_length -= 2

        return log


@adapter(IHarvester)
@implementer(IJson)
class JsonProcessor(BaseProcessor):
    """JSON Processor."""

    def get_data(self):
        url = self.harvester.url
        if not url:
            return []

        f = urllib.urlopen(url)
        resp = f.read()
        data = json.loads(resp)

        return data

    def read_fields(self, reread=False):
        if getattr(self.harvester, 'fields', None) and not reread:
            return self.harvester.fields

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

        self.harvester.fields = fields

        return fields

    def read_values(self):

        raw_data = self.read_raw_data()
        raw_data = self.clean_data_by_field(raw_data)
        raw_data = self.sort_raw_data(raw_data)

        self.cleaned_data = DataManager(raw_data)

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
        return subdata

    def read_raw_data(self):
        """

        :return: data dict like
        {field_identifier: list of values}
        """
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

    def sort_raw_data(self, raw_data):
        """

        :param raw_data: dict like {field_identifier: list of values}
        :return:
        dict like {ct_identifier: {index: {field: list of data}}}
        """
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

            if field_data is None:
                continue

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

        return data
