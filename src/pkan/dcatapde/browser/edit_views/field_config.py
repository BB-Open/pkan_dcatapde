from pkan.dcatapde.api.harvester import add_missing_fields
from pkan.dcatapde.content.harvester_field_config import IHarvesterFieldConfig
from plone.dexterity.browser import edit


class FieldConfigEdit(edit.DefaultEditForm):

    schema = IHarvesterFieldConfig

    def applyChanges(self, data):

        data['fields'] = add_missing_fields(self.context, data['fields'])

        return super(FieldConfigEdit, self).applyChanges(data)
