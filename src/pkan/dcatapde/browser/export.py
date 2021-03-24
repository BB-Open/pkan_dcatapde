# -*- coding: utf-8 -*-
from pkan.dcatapde.io.rdf.export import RDFMarshaller
from unidecode import unidecode

import os


try:
    LIMIT = int(os.environ.get('RDF_UNICODE_LIMIT', 65535))
except Exception:  # noqa: B902
    LIMIT = 65535   # Refs #83543 - Default: 0xFFFF, 2^16, 16-bit


class RDFExport(object):
    """ RDF Export """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _sanitize(self, utext, limit=LIMIT):
        """ Sanitize unicode text
        """
        for char in utext:
            if ord(char) > limit:
                yield unidecode(char)
            else:
                yield char

    def sanitize(self, text):
        """ Remove
        """
        if not isinstance(text):
            text = text.decode('utf-8')

        # Fast sanitize ASCII text
        try:
            text.encode()
        except Exception:  # noqa: B902
            return u''.join(self._sanitize(text))
        else:
            return text

    def __call__(self):
        marshaller = RDFMarshaller()
        endLevel = int(self.request.get('endLevel', 3))
        _content_type, _length, data = marshaller.marshall(self.context,
                                                           endLevel=endLevel)

        self.request.response.setHeader('Content-Type',
                                        'application/rdf+xml; charset=utf-8')
        return self.sanitize(data)
