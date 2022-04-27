import sys
from traceback import format_tb

import pkan_config.config as pkan_cfg
from iso2dcat.main import Main
from pyrdf4j.errors import URINotReachable
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth
from requests.exceptions import SSLError

from pkan.dcatapde import _
from pkan.dcatapde.harvesting.errors import NoSourcesDefined
from pkan.dcatapde.utils import LiteralHandler


def get_config(harvester):
    harvester = harvester
    cfg = pkan_cfg.get_plone_harvester_config_by_name(harvester.config)
    cfg.DCM_URI = harvester.dcm_url
    cfg.CSW_URI = harvester.csw_url
    cfg.CSW_OUTPUT_SCHEMA = harvester.csw_output_schema
    cfg.FALLBACK_CATALOG_NAME = harvester.fallback_name
    cfg.FALLBACK_URL = harvester.fallback_url
    return cfg


class GeodataRDFProcessor():

    def __init__(self, harvester):
        self.harvester = harvester
        self.literal_handler = LiteralHandler()

    def prepare_harvest(self, visitor):
        """Load data to be harvested into a temperary namespace
                on the tripelstore.
                Then set a rdflib grpah instance to it for reading.
                Open a target namespace for the dcat-ap.de compatible data and
                set a rdflib grpah instance to it for writing and reading.
                """

        self.def_lang = 'de'

        self.tripel_db_name = self.harvester.id_in_tripel_store
        self.tripel_temp_db_name = self.tripel_db_name + '_temp'
        self.tripel_dry_run_db = self.tripel_db_name + '_dryrun'

        cfg = pkan_cfg.get_config()

        self._rdf4j = RDF4J(rdf4j_base=cfg.RDF4J_BASE)
        self.auth = HTTPBasicAuth(cfg.ADMIN_USER, cfg.ADMIN_PASS)

        if visitor.real_run:
            self._rdf4j.create_repository(self.tripel_temp_db_name, repo_type=cfg.RDF_REPO_TYPE, overwrite=True,
                                          auth=self.auth)
            self.temp = self.tripel_temp_db_name
            self.target = self.tripel_db_name
        else:

            self._rdf4j.create_repository(self.tripel_dry_run_db, repo_type=cfg.RDF_REPO_TYPE, overwrite=True,
                                          auth=self.auth)
            self.temp = self.tripel_dry_run_db
            self.target = None

        self.config = get_config(self.harvester)
        self.config.WRITE_TO = self.temp
        self.config.ADMIN_USER = cfg.ADMIN_USER
        self.config.ADMIN_PASS = cfg.ADMIN_PASS
        self.config.RDF4J_BASE = cfg.RDF4J_BASE
        if not visitor.real_run:
            self.config.PARALLEL = False
        # todo: Read Information from Harvester

    @property
    def rdf4j(self):
        """Interface to incoming RDF graph"""
        return self._rdf4j

    def prepare_and_run(self, visitor):
        visitor.scribe.write(level='info', msg='Starting Harvest')
        try:
            self.prepare_harvest(visitor)
        except NoSourcesDefined:
            msg = u'No Sources found'
            visitor.scribe.write(
                level='error',
                msg=msg,
            )
            return
        except URINotReachable:
            msg = u'Sources or Database not reachable. Skipping.'
            visitor.scribe.write(
                level='error',
                msg=msg,
            )
            exc_type, exc_value, exc_traceback = sys.exc_info()
            msg = u"GET termiated due to error %s %s" % (exc_type, exc_value)
            visitor.scribe.write(
                level='error',
                msg=msg,
            )
            return

        if visitor.real_run:
            msg = u'starting harvest real run'
        else:
            msg = u'starting harvest dry run'
        visitor.scribe.write(
            level='info',
            msg=msg,
        )

        msg = _(u'Reading {kind} file')
        visitor.scribe.write(
            level='info',
            msg=msg,
            kind='Geodata',
        )
        try:
            Main().run(visitor=visitor, cfg=self.config)
        except SSLError:
            msg = _(u'{kind} file not read succesfully cause of SSLError')
            visitor.scribe.write(
                level='error',
                msg=msg,
                kind='Geodata',
            )
            for line in format_tb(sys.exc_info()[2]):
                visitor.scribe.write(
                    level='error',
                    msg='{error}',
                    error=line,
                )
            if self.target:
                msg = _(u'{kind} Skip writing data to final DB {target}')
                visitor.scribe.write(
                    level='error',
                    msg=msg,
                    kind='Geodata',
                    target = self.target
                )
            return

        msg = _(u'{kind} file read succesfully')
        visitor.scribe.write(
            level='info',
            msg=msg,
            kind='Geodata',
        )

        if self.target:
            msg = _(u'{kind} Copy data to final DB {target}')
            visitor.scribe.write(
                level='info',
                msg=msg,
                kind='Geodata',
                target=self.target
            )
            self.copy_data_to_target()

        if visitor.real_run:
            msg = u'Finished harvest real run'
        else:
            msg = u'Finished harvest dry run'
        visitor.scribe.write(
            level='info',
            msg=msg,
        )

        return visitor.scribe.html_log()

    def copy_data_to_target(self):
        cfg = pkan_cfg.get_config()
        self.rdf4j.create_repository(self.target, repo_type=cfg.RDF_REPO_TYPE, overwrite=True, auth=self.auth)
        self.rdf4j.move_data_between_repositorys(self.target, self.temp, self.auth, repo_type=cfg.RDF_REPO_TYPE)
