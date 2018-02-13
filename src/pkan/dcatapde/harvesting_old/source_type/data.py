# -*- coding: utf-8 -*-


class DataManager(object):

    def __init__(self, raw_data):
        self.created = {}
        self.data = {}
        self.cts = []
        self.ids = []
        self.data_amount = 0
        self.setup(raw_data)

    def setup(self, raw_data):
        self.cts = raw_data.keys()
        if not self.cts:
            return
        self.data_amount = len(raw_data[self.cts[0]])
        for ct in self.cts:
            if len(raw_data[ct]) > self.data_amount:
                self.data_amount = len(raw_data[ct])
        for x in range(self.data_amount):
            self.ids.append('data_id_' + str(x))

        self.ids = sorted(self.ids)

        self.setup_data(raw_data)

    def setup_data(self, raw_data):
        for ct in raw_data:
            self.data[ct] = {}
            for key in raw_data[ct].keys():
                field_data = raw_data[ct][key]
                id = self.ids[key]
                self.data[ct][id] = {}
                for field in field_data.keys():
                    data = field_data[field]
                    self.data[ct][id][field] = DataEntry(*data)

    def clean_duplicates(self):
        for ct in self.cts:
            ct_data = {}
            for id in self.ids:
                data_str = str(self.data[ct][id])
                if data_str in ct_data:
                    self.data[ct][id] = ct_data[data_str]
                else:
                    ct_data[data_str] = id

    def reset_attribute(self, ct, id, field, payload=None, field_name=None):
        # can be used to set or reset data
        if ct not in self.data:
            self.data[ct] = {}
        if id not in self.data[ct]:
            self.data[ct][id] = {}
        if field not in self.data[ct][id]:
            self.data[ct][id][field] = DataEntry(
                payload,
                field_name,
            )
        else:
            entry = self.data[ct][id][field]
            if payload:
                entry.payload = payload
            if field_name:
                entry.field_name = field_name

    def get_data_for_ct(self, ct):
        if ct not in self.cts:
            return []
        else:
            data = self.data[ct]
            new_data = {}
            for id in self.ids:
                if data[id] in self.ids:
                    pass
                else:
                    new_data[id] = {}
                    for field in data[id]:
                        new_data[id][field] = data[id][field].payload

        return new_data

    def set_created_obj(self, ct, id, obj):
        if ct not in self.created:
            self.created[ct] = {}
        if id not in self.created[ct]:
            self.created[ct][id] = obj
        elif obj is not None:
            self.created[ct][id] = obj

    def get_created(self, ct, id):
        if ct not in self.created:
            return None
        if id not in self.created[ct]:
            id = self.data[ct][id]
        return self.created[ct][id]

    def get_all_created(self, ct):
        if ct not in self.created:
            return {}
        return self.created[ct]

    def update(self, ct, id, data):
        # used for update multiple fields
        for field in data:
            self.reset_attribute(
                ct,
                id,
                field,
                payload=data[field],
            )

    def get_data_for_field(self, ct, id, field):
        if ct not in self.data:
            return None
        elif id not in self.data[ct]:
            return None
        elif field not in self.data[ct][id]:
            return None
        else:
            return self.data[ct][id][field]


class DataEntry(object):

    def __init__(self, payload, field_name):
        self.payload = payload
        self.field_name = field_name

    def __repr__(self):
        return str(self.payload) + '::' + str(self.field_name)
