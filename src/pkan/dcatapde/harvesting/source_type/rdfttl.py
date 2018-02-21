# -*- coding: utf-8 -*-
"""Harvesting adapter."""
from pkan.dcatapde import _
from pkan.dcatapde.constants import RDF_FORMAT_JSONLD
from pkan.dcatapde.constants import RDF_FORMAT_METADATA
from pkan.dcatapde.constants import RDF_FORMAT_TURTLE
from pkan.dcatapde.constants import RDF_FORMAT_XML
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.RDF.interfaces import IRDF
from pkan.dcatapde.harvesting.source_type.interfaces import IRDFJSONLD
from pkan.dcatapde.harvesting.source_type.interfaces import IRDFTTL
from pkan.dcatapde.harvesting.source_type.interfaces import IRDFXML
from pkan.dcatapde.log.log import TranslatingFormatter
from plone.api import portal
from rdflib import Graph
from rdflib.store import Store
from zope.component import adapter
from zope.interface import implementer

import io
import logging


IFaceToRDFFormat = {
    IRDFTTL: RDF_FORMAT_TURTLE,
    IRDFJSONLD: RDF_FORMAT_JSONLD,
    IRDFXML: RDF_FORMAT_XML,
}


@adapter(IHarvester)
@implementer(IRDFTTL)
class RDFProcessor(object):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    def __init__(self, harvester):
        # remember the harvester
        self.harvester = harvester
        # look if we have a harvesting type adapter
        try:
            self.harvesting_type = \
                self.harvester.harvesting_type(self.harvester)
        except TypeError:
            self.harvesting_type = None

        # fetch the preprocessor adapter
        self.data_cleaner = self.harvester.data_cleaner(self.harvester)
        self.cleaned_data = None
        # self.field_config = get_field_config(self.harvester)
        self.context = portal.get()
        if self.harvester:
            if self.harvester.base_object:
                # Todo: check why sometime to_object and sometimes not
                self.context = getattr(self.harvester.base_object,
                                       'to_object',
                                       self.harvester.base_object)

        # determine the source format serializer string for rdflib from our
        # own interface. Todo this is a bit ugly
        self.rdf_format_key = IFaceToRDFFormat[self.harvester.source_type]
        self.rdf_format = RDF_FORMAT_METADATA[self.rdf_format_key]
        self.serialize_format = self.rdf_format['serialize_as']
        self.setup_logger()

        # remember rdf_store
        self.rdfstore = None

    def read_rdf_file(self, uri, format):
        """Load the rdf data"""
        self.rdfstore = Store()
        # self.session = self.rdfstore.session
        # self.rdfstore.store.load_triples(source=uri, format=format)
        self.graph = Graph(self.rdfstore)
        self.graph.open(uri)
        self.graph.load(uri)

    def read_classes(self):
        """Read the classes of the rdf data for the vocabulary to assign
         to DX classes"""
        uri = self.harvester.url
        self.read_rdf_file(uri, self.serialize_format)
        SPARQL = """SELECT DISCTINCT ?o WHERE {?s a ?o .}"""
        result = self.graph.query(SPARQL)
        return result

    def run_query(self, query):
        if not self.rdfstore:
            self.read_rdf_file(self.harvester.url, self.serialize_format)
        result = self.graph.query(query)
        return result

    def read_dcat_fields(self, *args, **kwargs):
        """Dummy"""
        return []

    def read_fields(self, *args, **kwargs):
        """Dummy"""
        return []

    def clean_data(self, *arg, **kwargs):
        """Dummy"""

    def setup_logger(self):
        """Log to a io.stream that can later be embedded in the view output"""
        # get a logger named after the serializing format we use
        log = logging.getLogger(self.serialize_format)
        # get and remember the stream
        self.log_stream = io.StringIO()
        # construct a streamhandler
        stream_handler = logging.StreamHandler(self.log_stream)
        # and a formatter for HTML output
        format = '<p>%(asctime)s - %(name)s - %(levelname)s - %(message)s</p>'
        request = getattr(self.context, 'REQUEST', None)
        formatter = TranslatingFormatter(format, request=request)
        # and plug things together
        stream_handler.setFormatter(formatter)
        log.addHandler(stream_handler)
        self.log = log

    def reap_logger(self):
        """return the log output"""
        # rewind the stream
        self.log_stream.seek(0)
        # read the stream into a string
        log = self.log_stream.read()
        # get rid of the stream
        self.log_stream.close()
        # and return return the log
        return log

    def dry_run(self):
        """Dry Run: Returns Log-Information.
        """
        self.log.info(u'starting harvestdry run')
        uri = self.harvester.url

        msg = _(
            u'Reading ${kind} file ${uri}',
            mapping={'kind': self.serialize_format, 'uri': uri},
        )
        self.log.info(msg)
        self.read_rdf_file(uri, self.serialize_format)
        msg = _(
            u'${kind} file ${uri} read succesfully',
            mapping={'kind': self.serialize_format, 'uri': uri},
        )
        self.log.info(msg)
        self.log.info(u'Harvesting real run successfully')

        return self.reap_logger()

    def real_run(self):
        """Dry Run: Returns Log-Information.
        """
        self.log.info(u'Starting real harvest run')
        uri = self.harvester.url

        msg = _(
            u'Reading ${kind} file ${uri} into rdflib',
            mapping={'kind': self.serialize_format, 'uri': uri},
        )
        self.log.info(msg)
        self.read_rdf_file(uri, self.serialize_format)
        msg = _(
            u'${kind} file ${uri} read successfully into rdflib',
            mapping={'kind': self.serialize_format, 'uri': uri},
        )

        # Todo: self.data_type is data_cleaner and should not crawl the data
        # Todo: replace by correct adapter-layer
        # self.data_type.crawl(self.rdfstore)
        crawler = IRDF(self.harvester)
        crawler.crawl()

        self.log.info(u'Real harvest run successfull')

        return self.reap_logger()
