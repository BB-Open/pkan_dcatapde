# -*- coding: utf-8 -*-
from pkan.dcatapde.api.harvester import add_missing_fields
from pkan.dcatapde.content.harvester_field_config import IHarvesterFieldConfig
from plone.dexterity.browser import edit


class FieldConfigEdit(edit.DefaultEditForm):

    schema = IHarvesterFieldConfig

    def applyChanges(self, data):
        fields = data['fields']

        # first apply all other settings because they can influence required
        # fields
        del data['fields']
        applied = super(FieldConfigEdit, self).applyChanges(data)

        # clean fields with new settings
        fields = add_missing_fields(self.context, fields)
        # apply them
        self.context.fields = fields

        return applied
