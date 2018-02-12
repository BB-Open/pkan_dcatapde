# -*- coding: utf-8 -*-
"""RDF view."""

# from pkan.dcatapde.marshall.source.interfaces import IDX2Any
from pkan.dcatapde.marshall.interfaces import IMarshallSource
from pkan.dcatapde.marshall.target.rdf import RDFMarshallTarget
from unidecode import unidecode
from zope.component import queryMultiAdapter

import os


try:
    LIMIT = int(os.environ.get('RDF_UNICODE_LIMIT', 65535))
except Exception:
    LIMIT = 65535   # Refs #83543 - Default: 0xFFFF, 2^16, 16-bit

FORMATS = {
    'JSON': {
        'serialize_as': 'json-ld',
        'mime_type': 'application/ld+json; charset=utf-8',
    },
    'TURTLE': {
        'serialize_as': 'turtle',
        'mime_type': 'text/turtle; charset=utf-8',
    },
    'XML': {
        'serialize_as': 'pretty-xml',
        'mime_type': 'application/rdf+xml; charset=utf-8',
    },
}


class RDF_XML(object):
    """RDF Export."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _sanitize(self, utext, limit=LIMIT):
        """Sanitize unicode text."""
        for char in utext:
            if ord(char) > limit:
                yield unidecode(char)
            else:
                yield char

    def sanitize(self, text):
        """Remove."""
        if not isinstance(text, unicode):
            text = text.decode('utf-8')

        # Fast sanitize ASCII text
        try:
            text.encode()
        except Exception:
            return u''.join(self._sanitize(text))
        else:
            return text

    def to_RDF(self, format):
        # Fix: Transform to adapter call
        target = RDFMarshallTarget()
        marshaller = queryMultiAdapter(
            (self.context, target),
            interface=IMarshallSource,
        )
        if not marshaller:
            return
        marshaller.marshall()

        self.request.response.setHeader(
            'Content-Type',
            FORMATS[format]['mime_type'],
        )
        data = target._store.reader.graph.serialize(
            format=FORMATS[format]['serialize_as'],
        )
        return self.sanitize(data)

    def __call__(self):
        result = self.to_RDF('XML')
        return result


class RDF_JSON(RDF_XML):
    """RDF Export in JSON notation"""

    def __call__(self):
        result = self.to_RDF('JSON')
        return result


class RDF_TURTLE(RDF_XML):
    """RDF Export in Turtle notation"""

    def __call__(self):
        result = self.to_RDF('TURTLE')
        return result
