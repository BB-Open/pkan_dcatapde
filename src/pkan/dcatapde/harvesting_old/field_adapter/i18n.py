# -*- coding: utf-8 -*-
from pkan.dcatapde import _
from pkan.dcatapde.harvesting.field_adapter.base import BaseField
from pkan.dcatapde.harvesting.field_adapter.interfaces import IFieldProcessor
from plone import api
from plone.api.portal import get_current_language
from Products.CMFPlone.utils import safe_unicode
from ps.zope.i18nfield.interfaces import II18NTextField
from ps.zope.i18nfield.interfaces import II18NTextLineField
from zope.component import adapter
from zope.i18n import translate
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm


@adapter(II18NTextField)
@implementer(IFieldProcessor)
class I18nTextAdapter(BaseField):
    """
    """
    suffix = [_(u'language'), _(u'content')]

    def get_terms_for_vocab(self, ct, field_name, prefix='', required=False):
        terms = []

        if not prefix:
            field_required = self.field.required
        else:
            field_required = required

        field_path = self.get_field_path(prefix, field_name)

        for suf in self.suffix:
            # Todo: Fix the requirement dependencies VJ
            if field_required and not (suf == self.suffix[0]):
                title = _('${field_path}: ${suffix} (required)',
                          mapping={
                              u'field_path': u'{0}'.format(field_path),
                              u'suffix': u'{0}'.format(suf),
                          },
                          )
                token = '{CT}__{field_name}__{suffix}__required'.format(
                    CT=prefix + ct, field_name=field_name, suffix=suf,
                )
                terms.append(
                    SimpleTerm(
                        value=token, token=token, title=translate(
                            title,
                            target_language=get_current_language()),
                    ),
                )
            else:
                title = _('${field_path}: ${suffix}',
                          mapping={
                              u'field_path': u'{0}'.format(field_path),
                              u'suffix': u'{0}'.format(suf),
                          },
                          )
                token = '{CT}__{field_name}__{suffix}'.format(
                    CT=prefix + ct, field_name=field_name, suffix=suf,
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

        if self.suffix[1] in field_id:
            content_id = field_id
            language_id = field_id.replace(self.suffix[1], self.suffix[0])
            new_id = field_id.replace('__' + self.suffix[1], '')
            new_values = []
            default_language = safe_unicode(api.portal.get_default_language())

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
                        new_content = safe_unicode(content[x][element_id])
                        if language:
                            if isinstance(language, list):
                                new_language = language[x][element_id]
                            else:
                                new_language = language[x]
                        else:
                            new_language = default_language
                        new_data[new_language] = new_content
                    new_values.append(new_data)
                elif (
                        isinstance(content[x], str) or
                        isinstance(content[x], unicode)
                ):
                    new_content = safe_unicode(content[x])
                    if language:
                        new_language = language[x]
                    else:
                        new_language = default_language
                    new_values.append({
                        new_language: new_content,
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
