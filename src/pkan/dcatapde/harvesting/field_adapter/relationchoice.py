# -*- coding: utf-8 -*-
from pkan.dcatapde.api.functions import get_terms_for_ct
from pkan.dcatapde.harvesting.field_adapter.base import BaseField
from pkan.dcatapde.harvesting.field_adapter.interfaces import IFieldProcessor
from z3c.relationfield.interfaces import IRelationChoice
from zope.component import adapter
from zope.interface import implementer


@adapter(IRelationChoice)
@implementer(IFieldProcessor)
class RelationAdapter(BaseField):
    '''
    '''

    def get_terms_for_vocab(self, ct, field_name, prefix=''):
        terms = []

        field_prefix = prefix + ct + ':' + field_name + ':'
        cts = self.get_cts_from_relfield(self.field, field_name)
        for ct in cts:
            terms += get_terms_for_ct(ct,
                                      prefix=field_prefix)

        return terms

    def get_cts_from_relfield(self, field, field_name):

        tagged_values = field.interface._Element__tagged_values
        widgets = tagged_values[u'plone.autoform.widgets']

        if field_name in widgets:
            params = widgets[field_name].params
            if ('pattern_options' in params) and (
                    'selectableTypes' in params['pattern_options']):
                return params['pattern_options']['selectableTypes']
            elif 'content_type' in params:
                return [params['content_type']]

        return []

    def clean_value(self, data, field_id):
        """
        Dry Run will never use this method because it uses field of subtype.
        """

        return data
