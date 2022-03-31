# -*- coding: utf-8 -*-
"""Harvesting adapter."""
# from pkan.blazegraph.api import tripel_store
from pkan.dcatapde.constants import RDF_FORMAT_METADATA
from pkan.dcatapde.content.transfer import ITransfer
from pkan.dcatapde.harvesting.manager.base import IFaceToRDFFormatKey
from pkan.dcatapde.harvesting.manager.interfaces import IRDFJSONLD
from pkan.dcatapde.harvesting.manager.interfaces import IRDFTTL
from pkan.dcatapde.harvesting.manager.interfaces import IRDFXML
from pkan.dcatapde.harvesting.processors.rdf_base import BaseRDFProcessor
from plone.api import content
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth
from zope.component import adapter
from zope.interface import implementer
import pkan_config.config as pkan_cfg


@adapter(ITransfer)
@implementer(IRDFTTL)
@implementer(IRDFJSONLD)
@implementer(IRDFXML)
class RDFProcessorTransfer(BaseRDFProcessor):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    def __init__(self, transfer, raise_exceptions=True):
        # remember the transfer
        self.transfer = transfer
        self.raise_exceptions = raise_exceptions
        # look if we have a harvesting type adapter
        # try:
        #     self.harvesting_type = \
        #         self.transfer.harvesting_type(self.transfer)
        # except TypeError:
        #     self.harvesting_type = None

        # fetch the preprocessor adapter
        # self.data_cleaner = self.transfer.data_cleaner(self.transfer)
        self.cleaned_data = None
        # self.field_config = get_field_config(self.transfer)
        self.harvesting_context = self.transfer
        if self.transfer:
            if getattr(self.transfer, 'base_object', None):
                self.harvesting_context = content.get(
                    UID=self.transfer.base_object,
                )

        # determine the source format serializer string for rdflib from our
        # own interface. Todo this is a bit ugly
        if self.transfer.source_type:
            self.rdf_format_key = \
                IFaceToRDFFormatKey[self.transfer.source_type]
            self.rdf_format = RDF_FORMAT_METADATA[self.rdf_format_key]
            self.serialize_format = self.rdf_format['serialize_as']
            self.mime_type = self.rdf_format['mime_type']

        self.tripel_tempdb = None    # Temporary tripel store
        self.tripeldb = None         # Tripestore for dcapt-ap.de data
        self._target_graph = None        # Target graph instance
        cfg = pkan_cfg.get_config()
        self.rdf4j = RDF4J(rdf4j_base=cfg.RDF4J_BASE)
        self.auth = HTTPBasicAuth(cfg.ADMIN_USER, cfg.ADMIN_PASS)

    def copy_from_url(self):
        """Load data to be harvested into a temperary namespace on the tripelstore.
        Then set a rdflib grpah instance to it for reading.
        Open a target namespace for the dcat-ap.de compatible data and
        set a rdflib grpah instance to it for writing and reading.
        """
        tripel_db_name = self.transfer.id_in_tripel_store
        cfg = pkan_cfg.get_config()
        self.rdf4j.create_repository(tripel_db_name, cfg.RDF_REPO_TYPE, accept_existing=True, auth=self.auth)

        response = self.rdf4j.bulk_load_from_uri(tripel_db_name, self.transfer.url, self.mime_type, clear_repository=False, auth=self.auth)

        response_text = 'Status Code: ' + str(response.status_code) + ' Content: ' + response.content.decode('utf-8')

        return response_text

    def copy_from_namespace(self):
        tripel_db_name = self.transfer.id_in_tripel_store
        cfg = pkan_cfg.get_config()
        response = self.rdf4j.move_data_between_repositorys(tripel_db_name, self.transfer.source_namespace, auth=self.auth, repo_type=cfg.RDF_REPO_TYPE)
        response_text = 'Status Code: ' + str(response.status_code) + ' Content: ' + response.content.decode('utf-8')

        return response_text

    def real_run(self):
        if self.transfer.url:
            return self.copy_from_url()
        elif self.transfer.source_namespace:
            return self.copy_from_namespace()
