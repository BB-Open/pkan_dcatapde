# -*- coding: utf-8 -*-
"""Utils"""
from pkan.dcatapde.utils import get_current_language
from pkan.dcatapde.utils import get_default_language
from plone.app.content.interfaces import INameFromTitle
from zope.interface import implementer


def I18NField2Unique(obj):
    """Expresses an i18Nfield as unique as possible as a string"""
    langs = sorted(obj.keys())
    result = []
    for lang in langs:
        result.append(lang + ':' + obj[lang])

    return ' '.join(result)


@implementer(INameFromTitle)
class NameFromDCTTitle(object):
    """Get name from alternative title."""

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        # find the title field of the content object
        title_field = self.context.Title()
        # if the title field is already unicode use it
        if isinstance(title_field, str):
            return title_field
        # if it is a string, convert it to unicode
        if isinstance(title_field, str):
            return str(title_field)
        # If not get title from i18nfield
        default_language = get_default_language()
        if default_language in title_field:
            return title_field[default_language]
        else:
            current_language = get_current_language()
            if current_language in title_field:
                return title_field[current_language]

        return title_field[title_field.keys()[0]]
