# -*- coding: utf-8 -*-
from pkan.dcatapde.harvesting.field_adapter.interfaces import IFieldProcessor
from plone.dexterity.utils import safe_unicode
from z3c.form.interfaces import IField
from zope.component import adapter
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm


@adapter(IField)
@implementer(IFieldProcessor)
class BaseField(object):

    def __init__(self, field):
        self.field = field

    def get_terms_for_vocab(self, ct, field_name, prefix='', required=False):
        terms = []

        if not prefix:
            field_required = self.field.required
        else:
            field_required = required

        if prefix:
            display_ct_parts = prefix.split(':')[1:]
            display_ct = ':'.join(display_ct_parts)
        else:
            display_ct = ''

        if field_required:
            title = '{CT} {field_name} required'.format(
                CT=display_ct, field_name=field_name,
            )
            token = '{CT}__{field_name}__required'.format(
                CT=prefix + ct, field_name=field_name,
            )
            terms.append(
                SimpleTerm(
                    value=token, token=token, title=title,
                ),
            )
        else:
            title = '{CT} {field_name}'.format(
                CT=display_ct, field_name=field_name,
            )
            token = '{CT}__{field_name}'.format(
                CT=prefix + ct, field_name=field_name,
            )
            terms.append(
                SimpleTerm(
                    value=token, token=token, title=title,
                ),
            )
        return terms

    def clean_value(self, data, field_id):

        new_values = []

        for value in data[field_id]:

            if isinstance(value, list):
                str_values = []
                for element in value:
                    if element is None:
                        str_values.append('')
                    else:
                        str_values.append(str(element))

                new_values.append(safe_unicode(' '.join(str_values)))
            else:
                new_values.append(safe_unicode(value))

        data[field_id] = new_values

        return data
