# -*- coding: utf-8 -*-
from pkan.dcatapde.harvesting.field_adapter.base import BaseField
from pkan.dcatapde.harvesting.field_adapter.interfaces import IFieldProcessor
from ps.zope.i18nfield.interfaces import II18NTextField
from ps.zope.i18nfield.interfaces import II18NTextLineField
from zope.component import adapter
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm


@adapter(II18NTextField)
@implementer(IFieldProcessor)
class I18nTextAdapter(BaseField):
    '''
    '''
    suffix = ['language', 'content']

    def get_terms_for_vocab(self, ct, field_name, prefix=''):
        terms = []

        for suf in self.suffix:
            if self.field.required:
                title = '{CT}: {field_name} {suffix} required'.format(
                    CT=prefix + ct, field_name=field_name, suffix=suf
                )
                token = '{CT}__{field_name}__{suffix}__required'.format(
                    CT=prefix + ct, field_name=field_name, suffix=suf
                )
                terms.append(
                    SimpleTerm(
                        value=token, token=token, title=title)
                )
            else:
                title = '{CT}: {field_name} {suffix}'.format(
                    CT=prefix + ct, field_name=field_name, suffix=suf
                )
                token = '{CT}__{field_name}__{suffix}'.format(
                    CT=prefix + ct, field_name=field_name, suffix=suf
                )
                terms.append(
                    SimpleTerm(
                        value=token, token=token, title=title)
                )

        return terms


adapter(II18NTextLineField)
implementer(IFieldProcessor)
class I18nTextLineAdapter(I18nTextAdapter):
    '''
    '''
