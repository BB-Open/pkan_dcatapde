# -*- coding: utf-8 -*-
from zope.component import getUtility
from zope.interface import provider
from zope.schema._bootstrapinterfaces import IContextAwareDefaultFactory
from zope.schema.interfaces import IVocabularyFactory


@provider(IContextAwareDefaultFactory)
def ConfigFieldDefaultFactory(context):
        if context and hasattr(context, 'fields'):
            fields = context.fields
        else:
            fields = []

        vocab_name = 'pkan.dcatapde.DcatFieldVocabulary'
        factory = getUtility(IVocabularyFactory, vocab_name)
        options = factory(context)

        for value in options.by_value.keys():
            if 'required' in value:
                fields.append(
                    {
                        'dcat_field': value,
                        'source_field': None,
                        'prio': 1,
                    }
                )

        return fields
