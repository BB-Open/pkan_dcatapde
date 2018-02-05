# -*- coding: utf-8 -*-
from pkan.dcatapde.harvesting.field_adapter.base import BaseField
from pkan.dcatapde.harvesting.field_adapter.interfaces import IFieldProcessor
from plone import api
from plone.dexterity.utils import safe_unicode
from ps.zope.i18nfield.interfaces import II18NTextField
from ps.zope.i18nfield.interfaces import II18NTextLineField
from zope.component import adapter
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm


@adapter(II18NTextField)
@implementer(IFieldProcessor)
class I18nTextAdapter(BaseField):
    """
    """
    suffix = ['language', 'content']

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

        for suf in self.suffix:
            if field_required:
                title = '{CT} {field_name} {suffix} required'.format(
                    CT=display_ct, field_name=field_name, suffix=suf,
                )
                token = '{CT}__{field_name}__{suffix}__required'.format(
                    CT=prefix + ct, field_name=field_name, suffix=suf,
                )
                terms.append(
                    SimpleTerm(
                        value=token, token=token, title=title,
                    ),
                )
            else:
                title = '{CT} {field_name} {suffix}'.format(
                    CT=display_ct, field_name=field_name, suffix=suf,
                )
                token = '{CT}__{field_name}__{suffix}'.format(
                    CT=prefix + ct, field_name=field_name, suffix=suf,
                )
                terms.append(
                    SimpleTerm(
                        value=token, token=token, title=title,
                    ),
                )

        return terms

    def clean_value(self, data, field_id):

        if self.suffix[1] in field_id:
            content_id = field_id
            language_id = field_id.replace(self.suffix[1], self.suffix[0])
            new_id = field_id.replace('__' + self.suffix[1], '')
            new_values = []
            default_language = api.portal.get_default_language()

            content = data[content_id]
            del data[content_id]
            if language_id in data:
                language = data[language_id]
                del data[language_id]
            else:
                language = None

            for x in range(len(content)):
                if isinstance(content[x], list):
                    new_data = {}
                    for element_id in range(len(content[x])):
                        new_content = safe_unicode(str(content[x][element_id]))
                        if language:
                            if isinstance(language, list):
                                new_language = language[x][element_id]
                            else:
                                new_language = language[x]
                        else:
                            new_language = default_language
                        new_data[new_content] = new_language
                    new_values.append(new_data)
                elif (
                        isinstance(content[x], str) or
                        isinstance(content[x], unicode)
                ):
                    new_content = safe_unicode(str(content[x]))
                    if language:
                        new_language = language[x]
                    else:
                        new_language = default_language
                    new_values.append({
                        new_content: new_language,
                    })
                else:
                    new_values.append({})

            data[new_id] = new_values

        return data


@adapter(II18NTextLineField)
@implementer(IFieldProcessor)
class I18nTextLineAdapter(I18nTextAdapter):
    """
    """
