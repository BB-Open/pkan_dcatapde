# -*- coding: utf-8 -*-
"""Field DX Default Factory."""

from pkan.dcatapde.vocabularies.dcat_field import DcatFieldVocabulary
from zope.interface import provider
from zope.schema._bootstrapinterfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def ConfigFieldDefaultFactory(context):
    """Default Factory."""
    fields = []

    vocab = DcatFieldVocabulary()
    options = vocab(context)

    for value in options.by_value.keys():
        if 'required' in value:
            fields.append(
                {
                    'dcat_field': value,
                    'source_field': None,
                    'prio': 1,
                },
            )

    return fields
