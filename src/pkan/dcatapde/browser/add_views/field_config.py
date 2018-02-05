# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde import utils
from pkan.dcatapde.api.harvester import add_harvester_field_config
from pkan.dcatapde.api.harvester import add_missing_fields
from pkan.dcatapde.constants import CT_HARVESTER_FIELD_CONFIG
from plone.dexterity.browser import add
from z3c.form import button


class FieldConfigAddForm(add.DefaultAddForm):
    portal_type = CT_HARVESTER_FIELD_CONFIG

    def __init__(self, context, request, ti=None):
        super(FieldConfigAddForm, self).__init__(context, request)
        utils.set_request_annotations('pkan.vocabularies.context', context)

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
