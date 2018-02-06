# -*- coding: utf-8 -*-
from pkan.dcatapde import utils
from pkan.dcatapde.api.harvester import add_missing_fields
from pkan.dcatapde.api.harvester import update_field_config_form_fields
from pkan.dcatapde.content.harvester_field_config import CT_FIELD_RELATION
from pkan.dcatapde.content.harvester_field_config import IHarvesterFieldConfig
from plone.dexterity.browser import edit


class FieldConfigEdit(edit.DefaultEditForm):

    schema = IHarvesterFieldConfig

    def __init__(self, context, request, ti=None):
        super(FieldConfigEdit, self).__init__(context, request)
        utils.set_request_annotations('pkan.vocabularies.context', context)

    def update(self):
        self.fields = update_field_config_form_fields(self.context)

        super(FieldConfigEdit, self).update()

    def applyChanges(self, data):
        fields = {}

        for ct in CT_FIELD_RELATION.keys():
            field = CT_FIELD_RELATION[ct]
            if field in data:
                fields[ct] = data[field]
                del data[field]

        # first apply all other settings because they can influence required
        # fields
        applied = super(FieldConfigEdit, self).applyChanges(data)

        for ct in fields.keys():
            # clean fields with new settings
            ct_fields = add_missing_fields(fields[ct], ct=ct)
            # apply them
            setattr(self.context, CT_FIELD_RELATION[ct], ct_fields)

        return applied
