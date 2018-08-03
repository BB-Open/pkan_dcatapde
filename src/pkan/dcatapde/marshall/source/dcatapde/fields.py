# -*- coding: utf-8 -*-
"""DCATAP-DE Fields."""

from pkan.dcatapde.marshall.interfaces import IMarshallSource
from pkan.dcatapde.marshall.source.dcatapde.dcat2rdf import DCATField2RDF
from pkan.dcatapde.marshall.target.interfaces import IRDFMarshallTarget
from pkan.dcatapde.utils import get_available_languages_iso
from pkan.dcatapde.utils import get_default_language
from ps.zope.i18nfield.field import I18NField
from zope.component import adapter
from zope.interface import implementer

import rdflib


@implementer(IMarshallSource)
@adapter(I18NField, IRDFMarshallTarget)
class I18NField2RDF(DCATField2RDF):
    """Default marshaller for I18Nfields."""

    def marshall_myself(self, obj):
        """Marshall myself."""
        # get value of the field
        field_value = self.field
        langs = get_available_languages_iso()

        # The field emit a list of literals
        literals = []
        if field_value is not None:
            for lang, text in field_value.items():
                if lang == u'__default_value':
                    lang = get_default_language()
                if lang in langs.values():
                    lang = list(langs.keys())[list(langs.values()).index(lang)]
                literal = rdflib.term.Literal(text, lang=lang)
                literals.append(literal)

        if not literals:
            return None
        return literals

    def marshall(self, obj):
        return self.marshall_myself(obj)


@implementer(IMarshallSource)
@adapter(IRDFMarshallTarget)
class ADMS_IDINTIFIER2RDF(DCATField2RDF):
    """Marshall adms_identifier None Values as link to local data"""

    def __init__(self, context, marshall_target):
        """Initialization.

        :param context: Content object to start crawl
        :param marshall_target: marshalling target e.g. an RDF store
        """
        self.context = context
        self.marshall_target = marshall_target

    def marshall_myself(self, obj):
        """Marshall myself."""
        # get value of the field
        field_value = self.context.adms_identifier
        if field_value is None:
            return self.context.absolute_url()
        else:
            return field_value


@implementer(IMarshallSource)
@adapter(IRDFMarshallTarget)
class DCT_IDINTIFIER2RDF(DCATField2RDF):
    """Marshall adms_identifier None Values as link to local data"""

    def __init__(self, context, marshall_target):
        """Initialization.

        :param context: Content object to start crawl
        :param marshall_target: marshalling target e.g. an RDF store
        """
        self.context = context
        self.marshall_target = marshall_target

    def marshall_myself(self, obj):
        """Marshall myself."""
        # get value of the field
        field_value = self.context.dct_identifier
        if field_value is None:
            return self.context.absolute_url()
        else:
            return field_value
