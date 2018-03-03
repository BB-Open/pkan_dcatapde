# -*- coding: utf-8 -*-
"""Utils"""
from pkan.dcatapde.structure.interfaces import IStructure
from plone.api import portal
from plone.app.content.interfaces import INameFromTitle
from zope.interface import implementer


def I18NField2Unique(obj):
    """Expresses an i18Nfield as unique as possible as a string"""
    langs = obj.keys()
    langs.sort()
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
        struct = IStructure(self.context)
        try:
            title_field = getattr(self.context, struct.title_field)
        except:
            return ''
        # if the title field is already unicode use it
        if isinstance(title_field, unicode):
            return title_field
        # If not get title from i18nfield
        default_language = portal.get_default_language()[:2]
        if default_language in title_field:
            return title_field[default_language]
        else:
            current_language = portal.get_current_language()[:2]
            if current_language in title_field:
                return title_field[current_language]

        return title_field[title_field.keys()[0]]
