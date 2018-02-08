# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.harvesting.field_adapter.interfaces import IFieldProcessor
from plone.api.portal import get_current_language
from plone.dexterity.utils import safe_unicode
from z3c.form.interfaces import IField
from zope.component import adapter
from zope.i18n import translate
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm


@adapter(IField)
@implementer(IFieldProcessor)
class BaseField(object):

    def __init__(self, field):
        self.field = field

    def get_field_path(self, prefix, field_name):
        if prefix:
            display_ct_parts = prefix.split(':')[1:]
        else:
            display_ct_parts = []

        display_ct_parts = filter(lambda a: a != '', display_ct_parts)

        display_ct_parts.append(field_name)
        field_path = '=>'.join(display_ct_parts)
        return field_path

    def get_terms_for_vocab(self, ct, field_name, prefix='', required=False):
        terms = []

        if not prefix:
            field_required = self.field.required
        else:
            field_required = required

        field_path = self.get_field_path(prefix, field_name)

        if field_required:
            title = _('${field_path} (required)',
                      mapping={
                          u'field_path': u'{0}'.format(field_path),
                      },
                      )

            token = '{CT}__{field_name}__required'.format(
                CT=prefix + ct, field_name=field_name,
            )
            terms.append(
                SimpleTerm(
                    value=token, token=token, title=translate(
                        title,
                        target_language=get_current_language()),
                ),
            )
        else:
            title = _('${field_path}',
                      mapping={
                          u'field_path': u'{0}'.format(field_path),
                      },
                      )
            token = '{CT}__{field_name}'.format(
                CT=prefix + ct, field_name=field_name,
            )
            terms.append(
                SimpleTerm(
                    value=token, token=token, title=translate(
                        title,
                        target_language=get_current_language()),
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
