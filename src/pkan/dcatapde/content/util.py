# -*- coding: utf-8 -*-
"""Utils"""


def I18NField2Unique(obj):
    """Expresses an i18Nfield as unique as possible as a string"""
    langs = obj.keys()
    langs.sort()
    result = []
    for lang in langs:
        result.append(lang + ':' + obj[lang])

    return ' '.join(result)
