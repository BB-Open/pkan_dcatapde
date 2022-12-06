# -*- coding: utf-8 -*-

"""Harvesting adapter."""
import datetime

import pkan_config.config as pkan_cfg
# from pkan.blazegraph.api import tripel_store
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth

from pkan.dcatapde.harvesting.errors import NoSourcesDefined
from pkan.dcatapde.harvesting.load_data.rdf_base import BaseRDFProcessor
from pkan.dcatapde.constants import COMPLETE_SUFFIX


class TripleStoreRDFProcessor(BaseRDFProcessor):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    def prepare_and_run(self, visitor):
        """Load data to be harvested into a temperary namespace
        on the tripelstore.
        Then set a rdflib grpah instance to it for reading.
        Open a target namespace for the dcat-ap.de compatible data and
        set a rdflib grpah instance to it for writing and reading.
        """
        # todo: Missing Attribute, should it be 2 or 3 letters?
        #  Should be set by harvester
        cfg = pkan_cfg.get_config()

        self.def_lang = 'de'

        self.tripel_db_name = self.harvester.id_in_tripel_store + COMPLETE_SUFFIX

        # todo: base in constants
        self._rdf4j = RDF4J(rdf4j_base=cfg.RDF4J_BASE)
        self.auth = HTTPBasicAuth(cfg.ADMIN_USER, cfg.ADMIN_PASS)

        # todo: Type in constants, is this correct type
        self._rdf4j.create_repository(self.tripel_db_name, repo_type=cfg.RDF_REPO_TYPE, overwrite=False, accept_existing=True, auth=self.auth)

        # self._graph, _response = tripel_store.graph_from_uri(
        #     tripel_temp_db_name,
        #     self.harvester.url,
        #     self.harvester.mime_type,
        #     clear_namespace=True,
        # )
        # tripel_store.empty_namespace(tripel_db_name)
        # self._target_graph = tripel_store.create_namespace(tripel_db_name)
        self.query_db = self.tripel_db_name


        msg = u'Working on {url}'.format(url=self.harvester.url)
        visitor.scribe.write(
            level='info',
            msg=msg,
        )

        self._rdf4j.bulk_load_from_uri(self.query_db, self.harvester.url, self.harvester.mime_type, auth=self.auth, clear_repository=True)
        self.harvester.last_run = datetime.datetime.now()
        msg = u'Loaded {url}'.format(url=self.harvester.url)
        visitor.scribe.write(
            level='info',
            msg=msg,
        )

        self.add_contributer_id(visitor, self._rdf4j, self.auth, [self.query_db])

        msg = u'Finished Real Run'
        visitor.scribe.write(
            level='info',
            msg=msg,
        )


class MultiUrlTripleStoreRDFProcessor(BaseRDFProcessor):

    def prepare_and_run(self, visitor):
        """Load data to be harvested into a temperary namespace
                on the tripelstore.
                Then set a rdflib grpah instance to it for reading.
                Open a target namespace for the dcat-ap.de compatible data and
                set a rdflib grpah instance to it for writing and reading.
                """

        cfg = pkan_cfg.get_config()

        self.def_lang = 'de'

        sources = self.harvester.catalog_urls

        self.tripel_db_name = self.harvester.id_in_tripel_store
        self.tripel_temp_db_name = self.tripel_db_name + COMPLETE_SUFFIX

        # todo: base in constants
        self._rdf4j = RDF4J(rdf4j_base=cfg.RDF4J_BASE)
        self.auth = HTTPBasicAuth(cfg.ADMIN_USER, cfg.ADMIN_PASS)


        # todo: Type in constants, is this correct type
        self._rdf4j.create_repository(self.tripel_temp_db_name, repo_type=cfg.RDF_REPO_TYPE, overwrite=True,
                                      auth=self.auth)

        self.query_db = self.tripel_temp_db_name

        # todo: Missing Attribute, should it be 2 or 3 letters?
        #   Should be set by harvester
        if not self.harvester.catalog_urls:
            raise NoSourcesDefined('You did not define any sources')

        # append for all the others
        for source in sources:
            msg = u'Working on {url}'.format(url=source)
            visitor.scribe.write(
                level='info',
                msg=msg,
            )
            self._rdf4j.bulk_load_from_uri(self.query_db, source, self.harvester.mime_type, auth=self.auth)
            msg = u'Loaded {url}'.format(url=self.harvester.url)
            visitor.scribe.write(
                level='info',
                msg=msg,
            )

        self.add_contributer_id(visitor, self._rdf4j, self.auth, [self.query_db])

        msg = u'Finished Real Run'
        visitor.scribe.write(
            level='info',
            msg=msg,
        )