# -*- coding: utf-8 -*-
from pkan.dcatapde import utils
from pkan.dcatapde.api.harvester_entity import update_form_fields
from pkan.dcatapde.content.harvester_entity import CT_ENTITY_RELATION
from pkan.dcatapde.content.harvester_entity import IHarvesterEntity
from plone.dexterity.browser import edit


class EntityEdit(edit.DefaultEditForm):

    schema = IHarvesterEntity

    def __init__(self, context, request, ti=None):
        super(EntityEdit, self).__init__(context, request)
        utils.set_request_annotations('pkan.vocabularies.context', context)

    def update(self):
        self.fields = update_form_fields(self.context)

        super(EntityEdit, self).update()

    def applyChanges(self, data):
        fields = {}

        for ct in CT_ENTITY_RELATION.keys():
            field = CT_ENTITY_RELATION[ct]
            if field in data:
                fields[ct] = data[field]
                del data[field]

        # first apply all other settings because they can influence required
        # fields
        applied = super(EntityEdit, self).applyChanges(data)

        # for ct in fields.keys():
        #     # clean fields with new settings
        #     ct_fields = add_missing_fields(fields[ct], ct=ct)
        #     # apply them
        #     setattr(self.context, CT_ENTITY_RELATION[ct], ct_fields)

        return applied
