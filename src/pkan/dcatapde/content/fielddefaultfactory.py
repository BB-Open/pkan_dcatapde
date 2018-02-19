# -*- coding: utf-8 -*-
"""Field DX Default Factory."""
from pkan.dcatapde import utils
from pkan.dcatapde.vocabularies.dcat_field import DcatFieldVocabulary
from zope.interface import implementer
from zope.interface import provider
from zope.schema._bootstrapinterfaces import IContextAwareDefaultFactory
from zope.schema.interfaces import IContextSourceBinder


@provider(IContextAwareDefaultFactory)
@implementer(IContextSourceBinder)
class ConfigFieldDefaultFactory(object):
    """Default Factory."""

    def __init__(self, ct, context=None):
        self.ct = ct
        if context:
            utils.set_request_annotations('pkan.vocabularies.context', context)

    def __call__(self):
        fields = []

        context = None

        vocab = DcatFieldVocabulary([self.ct])
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
