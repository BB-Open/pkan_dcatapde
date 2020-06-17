# -*- coding: utf-8 -*-
"""RDF view."""

# from pkan.dcatapde.marshall.source.interfaces import IDX2Any
from pkan.dcatapde.constants import RDF_FORMAT_JSONLD
from pkan.dcatapde.constants import RDF_FORMAT_METADATA
from pkan.dcatapde.constants import RDF_FORMAT_TURTLE
from pkan.dcatapde.constants import RDF_FORMAT_XML
from pkan.dcatapde.marshall.interfaces import IMarshallSource
from pkan.dcatapde.marshall.target.rdf import RDFMarshallTarget
from unidecode import unidecode
from zope.component import queryMultiAdapter

import os


try:
    LIMIT = int(os.environ.get('RDF_UNICODE_LIMIT', 65535))
except Exception:
    LIMIT = 65535   # Refs #83543 - Default: 0xFFFF, 2^16, 16-bit


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
        if not isinstance(text, str):
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
            RDF_FORMAT_METADATA[format]['mime_type'],
        )
        self.request.response.setHeader(
            'Cache-Control',
            'no-cache, no-store, must-revalidate',
        )
        data = target._store.reader.graph.serialize(
            format=RDF_FORMAT_METADATA[format]['serialize_as'],
        )
        return self.sanitize(data)

    def __call__(self):
        result = self.to_RDF(RDF_FORMAT_XML)
        return result


class RDF_JSON(RDF_XML):
    """RDF Export in JSON notation"""

    def __call__(self):
        result = self.to_RDF(RDF_FORMAT_JSONLD)
        return result


class RDF_TURTLE(RDF_XML):
    """RDF Export in Turtle notation"""

    def __call__(self):
        result = self.to_RDF(RDF_FORMAT_TURTLE)
        return result
