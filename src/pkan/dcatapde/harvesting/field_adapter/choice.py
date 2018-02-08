# -*- coding: utf-8 -*-

from pkan.dcatapde.api.functions import get_terms_for_ct
from pkan.dcatapde.harvesting.field_adapter.base import BaseField
from pkan.dcatapde.harvesting.field_adapter.interfaces import IFieldProcessor
from zope.component import adapter
from zope.interface import implementer
from zope.schema.interfaces import IChoice


@adapter(IChoice)
@implementer(IFieldProcessor)
class ChoiceAdapter(BaseField):
    """
    Choices are used as Relations or as normal Choices. This Adapter checks
    both using widgets information.
    """
    def __init__(self, field):
        self.field = field

    def get_terms_for_vocab(self, ct, field_name, prefix='', required=False):
        terms = []

        if not prefix:
            field_required = self.field.required
        else:
            field_required = required

        field_prefix = prefix + ct + ':' + field_name + ':'
        cts = self.get_cts_from_relfield(self.field, field_name)
        # if no cts are found Choice is not presenting a relation
        if not cts:
            return super(ChoiceAdapter, self).get_terms_for_vocab(
                ct,
                field_name,
                prefix=prefix,
                required=required,
            )
        # else we get fields of subtype
        for target_ct in cts:
            if target_ct == ct:
                continue
            terms += get_terms_for_ct(target_ct,
                                      prefix=field_prefix,
                                      required=field_required)

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
        Dry Run will never use this method for Relations because it
        uses field of subtype.

        If this method is used, it must be a normal Choice, so data is
        cleaned like Default.
        """

        return super(ChoiceAdapter, self).clean_value(data, field_id)
