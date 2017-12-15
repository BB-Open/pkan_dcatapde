""" Surf conversion classes """

import re
from DateTime.DateTime import DateTime
from Products.CMFPlone import log
from chardet import detect
from .interfaces import IValue2Surf
from rdflib import URIRef
from zope.component import adapts
from zope.interface import implements, Interface


class Value2Surf(object):
    """Base implementation of IValue2Surf
    """
    implements(IValue2Surf)
    adapts(Interface)

    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwds):
        language = kwds['language']
        if isinstance(self.value, unicode):
            return (self.value, language)
        try:
            value = (unicode(self.value, 'utf-8', 'replace'), language)
        except TypeError:
            value = str(self.value)
        return value


class URIRef2Surf(Value2Surf):
    """ Value2Surf implementation for URIRef
    """
    adapts(URIRef)

    def __call__(self, *args, **kwargs):
        return self.value


class Tuple2Surf(Value2Surf):
    """IValue2Surf implementation for tuples.
    """
    adapts(tuple)

    def __call__(self, *args, **kwds):
        return list(self.value)


class List2Surf(Value2Surf):
    """IValue2Surf implementation for tuples.
    """
    adapts(list)

    def __call__(self, *args, **kwds):
        return self.value


class Set2Surf(Value2Surf):
    """IValue2Surf implementation for sets.
    """
    adapts(set)

    def __call__(self, *args, **kwds):
        return list(self.value)


class String2Surf(Value2Surf):
    """IValue2Surf implementation for strings
    """
    adapts(str)

    _illegal_xml_chars = re.compile(
        u'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]'
    )

    def escapeXMLIllegalCharacters(self):
        """Replaces all the XML illegal characters with spaces
        """
        return self._illegal_xml_chars.sub(' ', self.value)

    def __call__(self, *args, **kwds):
        # Stripped illegal xml characters from string
        self.value = self.escapeXMLIllegalCharacters()

        if not self.value.strip():
            return None
        nonEUencodings = ['Big5', 'GB2312', 'EUC-TW', 'HZ-GB-2312',
                          'ISO-2022-CN', 'EUC-JP', 'SHIFT_JIS', 'ISO-2022-JP',
                          'EUC-KR', 'ISO-2022-KR', 'TIS-620', 'ISO-8859-2']
        language = kwds['language']
        encoding = detect(self.value)['encoding']

        if encoding in nonEUencodings:
            value = self.value.decode('utf-8', 'replace')
        else:
            try:
                value = self.value.decode(encoding)
            except (LookupError, UnicodeDecodeError):
                log.log("Could not decode to %s in rdfmarshaller" %
                        encoding)
                value = self.value.decode('utf-8', 'replace')
        return (value.encode('utf-8').strip(), language)


class DateTime2Surf(Value2Surf):
    """IValue2Surf implementation for DateTime """

    adapts(DateTime)

    def __call__(self, *args, **kwds):
        return (self.value.HTML4(), None,
                'http://www.w3.org/2001/XMLSchema#dateTime')
