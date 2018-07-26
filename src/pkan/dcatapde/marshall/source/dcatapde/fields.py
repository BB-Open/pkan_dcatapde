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
