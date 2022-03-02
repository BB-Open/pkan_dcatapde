import sys

from pyrdf4j.errors import URINotReachable
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth

from pkan.dcatapde.constants import RDF4J_BASE, ADMIN_USER, ADMIN_PASS, RDF_REPO_TYPE
from pkan.dcatapde.harvesting.errors import NoSourcesDefined
from pkan.dcatapde.utils import LiteralHandler
from pkan.dcatapde import _



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
        self.tripel_dry_run_db = self.tripel_db_name + '_dryrun'

        # todo: base in constants
        self._rdf4j = RDF4J(rdf4j_base=RDF4J_BASE)
        self.auth = HTTPBasicAuth(ADMIN_USER, ADMIN_PASS)

        if visitor.real_run:
            self._rdf4j.create_repository(self.tripel_db_name, repo_type=RDF_REPO_TYPE, overwrite=True,
                                          auth=self.auth)
            self.target = self.tripel_db_name
        else:

            self._rdf4j.create_repository(self.tripel_dry_run_db, repo_type=RDF_REPO_TYPE, overwrite=True,
                                          auth=self.auth)
            self.target = self.tripel_dry_run_db

        # todo: Read Information from Harvester

    @property
    def rdf4j(self):
        """Interface to incoming RDF graph"""
        return self._rdf4j

    def prepare_and_run(self, visitor):
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

        # todo: Logic here

        msg = _(u'{kind} file read succesfully')
        visitor.scribe.write(
            level='info',
            msg=msg,
            kind='Geodata',
        )

        if visitor.real_run:
            msg = u'Finished harvest real run'
        else:
            msg = u'Finished harvest dry run'
        visitor.scribe.write(
            level='info',
            msg=msg,
        )

        return visitor.scribe.html_log()
