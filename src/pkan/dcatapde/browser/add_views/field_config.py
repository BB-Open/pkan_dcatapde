# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.api.harvester import add_harvester_field_config
from pkan.dcatapde.api.harvester import add_missing_fields
from pkan.dcatapde.constants import CT_HarvesterFieldConfig
from plone.dexterity.browser import add
from z3c.form import button


class FieldConfigAddForm(add.DefaultAddForm):
    portal_type = CT_HarvesterFieldConfig

    @button.buttonAndHandler(_('Save'), name='save')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _('Please correct errors')
            return

        data['fields'] = add_missing_fields(self.context, data['fields'])

        add_harvester_field_config(self.context, **data)


class FieldConfigAddView(add.DefaultAddView):
    form = FieldConfigAddForm
