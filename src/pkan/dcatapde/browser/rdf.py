# -*- coding: utf-8 -*-
import os

from pkan.dcatapde.marshall.crawler import Crawler
from pkan.dcatapde.marshall.targets.rdf import RDFMarshallTarget
from unidecode import unidecode

try:
    LIMIT = int(os.environ.get('RDF_UNICODE_LIMIT', 65535))
except Exception:
    LIMIT = 65535   # Refs #83543 - Default: 0xFFFF, 2^16, 16-bit


class RDF(object):
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
        if not isinstance(text, unicode):
            text = text.decode('utf-8')

        # Fast sanitize ASCII text
        try:
            text.encode()
        except Exception:
            return u''.join(self._sanitize(text))
        else:
            return text

    def __call__(self):
        marshaller = RDFMarshallTarget()
        crawler = Crawler( self.context, marshaller)
        crawler.crawl()

#        marshaller
#        endLevel = int(self.request.get('endLevel', 3))
#        _content_type, _length, data = marshaller.marshall(self.context,
#                                                           endLevel=endLevel)

        self.request.response.setHeader('Content-Type',
                                        'application/rdf+xml; charset=utf-8')
        data = marshaller._store.reader.graph.serialize(format='pretty-xml')
        return self.sanitize(data)
