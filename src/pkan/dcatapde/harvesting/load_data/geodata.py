# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pkan_config.config as pkan_cfg
from dynaconf import loaders
from dynaconf.utils.boxing import DynaBox
from pyrdf4j.errors import URINotReachable
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth

from pkan.dcatapde import _
from pkan.dcatapde.harvesting.errors import NoSourcesDefined, GeoHarvestingFailed
from pkan.dcatapde.utils import LiteralHandler
from pkan.dcatapde.constants import COMPLETE_SUFFIX, TEMP_SUFFIX


def get_config(harvester):
    harvester = harvester
    cfg = pkan_cfg.get_plone_harvester_config_by_name(harvester.config)
    if harvester.dcm_url:
        cfg.DCM_URI = harvester.dcm_url
    else:
        cfg.DCM_URI = None
    cfg.CSW_URI = harvester.csw_url
    cfg.CSW_OUTPUT_SCHEMA = harvester.csw_output_schema
    cfg.FALLBACK_CATALOG_NAME = harvester.fallback_name
    cfg.FALLBACK_URL = harvester.fallback_url
    return cfg


class GeodataRDFProcessor:

    def __init__(self, harvester):
        self.harvester = harvester
        self.literal_handler = LiteralHandler()

    def prepare_harvest(self, visitor):
        """Load data to be harvested into a complete store
                on the tripelstore.
                """

        self.def_lang = 'de'

        self.tripel_db_name = self.harvester.id_in_tripel_store
        self.tripel_temp_db_name = self.tripel_db_name + TEMP_SUFFIX

        self.cfg = pkan_cfg.get_config()

        self._rdf4j = RDF4J(rdf4j_base=self.cfg.RDF4J_BASE)
        self.auth = HTTPBasicAuth(self.cfg.ADMIN_USER, self.cfg.ADMIN_PASS)

        self._rdf4j.create_repository(self.tripel_temp_db_name, repo_type=self.cfg.RDF_REPO_TYPE, overwrite=True,
                                      auth=self.auth)
        self.temp = self.tripel_temp_db_name

        self.config = get_config(self.harvester)
        self.config.WRITE_TO = self.temp
        self.config.ADMIN_USER = self.cfg.ADMIN_USER
        self.config.ADMIN_PASS = self.cfg.ADMIN_PASS
        self.config.RDF4J_BASE = self.cfg.RDF4J_BASE

    def finalize(self, visitor):
        msg = u'Writing Data to Complete Store'
        visitor.scribe.write(
            level='info',
            msg=msg,
        )
        target = self.tripel_db_name + COMPLETE_SUFFIX
        self._rdf4j.create_repository(target, repo_type=self.cfg.RDF_REPO_TYPE, overwrite=True, auth=self.auth)
        self._rdf4j.move_data_between_repositorys(target, self.tripel_temp_db_name, auth=self.auth,
                                                  repo_type=self.cfg.RDF_REPO_TYPE)

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
            msg = u'GET termiated due to error {type} {val}'.format(
                type=exc_type,
                val=exc_value,
            )
            visitor.scribe.write(
                level='error',
                msg=msg,
            )
            return

        msg = u'starting harvest real run'

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
        file = tempfile.NamedTemporaryFile(suffix='.yaml')

        stat_file = tempfile.NamedTemporaryFile(suffix='.txt')
        loaders.write(file.name, DynaBox(self.config.as_dict(env='Default')).to_dict(), env='Default')
        package_dir = Path(os.path.abspath(__file__)).parent
        python_file = package_dir / 'run_iso2dcat.py'
        res = subprocess.run(
            [self.config.PYTHON_EXE, str(python_file), '--file', file.name, '--target', stat_file.name],
            capture_output=True)
        file.close()
        if res.returncode == 0:
            for line in stat_file.readlines():
                visitor.scribe.write(
                    level='info',
                    msg=line.decode(),
                    kind='Geodata'
                )
        else:
            msg = _(u'{kind} file not read succesfully cause of ReturnCode {code}')
            visitor.scribe.write(
                level='error',
                msg=msg,
                kind='Geodata',
                code=res.returncode
            )
            visitor.scribe.write(
                level='error',
                msg=res.stderr.decode(),
                kind='Geodata'
            )
            stat_file.close()

            raise GeoHarvestingFailed('Geo Harvesting Failed')
        stat_file.close()
        msg = _(u'{kind} file read succesfully')
        visitor.scribe.write(
            level='info',
            msg=msg,
            kind='Geodata',
        )

        msg = u'Finished harvest real run'

        visitor.scribe.write(
            level='info',
            msg=msg,
        )

        self.finalize(visitor)

        return visitor.scribe.html_log()
