# -*- coding: utf-8 -*-

from pkan.dcatapde.constants import DCAT_CT
from plone.dexterity.interfaces import IDexterityFTI
from z3c.relationfield import RelationChoice
from zope.component import getUtility
from zope.interface import implementer
from zope.schema import getFields
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class DcatFieldVocabulary(object):
    """
    """

    def __call__(self, context):
        terms = []
        for CT in DCAT_CT:
            terms = terms + self.get_terms_for_ct(CT)

        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)

    def get_terms_for_ct(self, CT, prefix=''):
        terms = []
        schema = getUtility(IDexterityFTI,
                            name=CT).lookupSchema()
        fields = getFields(schema)
        for field_name in fields.keys():
            field = fields[field_name]
            if isinstance(field, RelationChoice):
                field_prefix = CT + ':' + field_name + ':'
                cts = self.get_cts_from_relfield(field, field_name)
                for ct in cts:
                    terms += self.get_terms_for_ct(ct,
                                                   prefix=field_prefix)
            else:
                if field.required:
                    value = '{CT}__{field_name}__required'.format(
                        CT=prefix+CT, field_name=field_name
                    )
                    title = '{CT}: {field_name} required'.format(
                        CT=prefix+CT, field_name=field_name
                    )
                    terms.append(
                        SimpleTerm(
                            value=value, token=value, title=title)
                    )
                else:
                    value = '{CT}__{field_name}'.format(
                        CT=prefix+CT, field_name=field_name
                    )
                    title = '{CT}: {field_name}'.format(
                        CT=prefix+CT, field_name=field_name
                    )
                    terms.append(
                        SimpleTerm(
                            value=value, token=value, title=title)
                    )
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


DcatFieldVocabularyFactory = DcatFieldVocabulary()
