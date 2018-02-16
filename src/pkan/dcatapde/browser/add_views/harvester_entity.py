# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde import utils
from pkan.dcatapde.api.harvester_entity import add_harvester_entity
from pkan.dcatapde.api.harvester_entity import update_form_fields
from pkan.dcatapde.constants import CT_HARVESTER_ENTITY
from plone.dexterity.browser import add
from z3c.form import button


class EntityAddForm(add.DefaultAddForm):
    portal_type = CT_HARVESTER_ENTITY

    def __init__(self, context, request, ti=None):
        super(EntityAddForm, self).__init__(context, request)
        utils.set_request_annotations('pkan.vocabularies.context', context)

    def update(self):

        self.fields = update_form_fields(self.context)

        super(EntityAddForm, self).update()

    @button.buttonAndHandler(_('Save'), name='save')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _('Please correct errors')
            return

        config = add_harvester_entity(self.context, **data)

        self.request.response.redirect(config.absolute_url())


class EntityAddView(add.DefaultAddView):
    form = EntityAddForm
