from pkan.dcatapde.constants import ERROR_SUFFIX, COMPLETE_SUFFIX
from pkan.dcatapde.harvesting.load_data.rdf_base import BaseRDFProcessor
from shacl.validate import ValidationRun
from shacl.log.log import unregister_logger, get_logger


class TripleStoreRDFValidator(BaseRDFProcessor):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    def prepare_and_run(self, visitor):
        """Load data to be harvested into a temperary namespace
        on the tripelstore.
        Then set a rdflib grpah instance to it for reading.
        Open a target namespace for the dcat-ap.de compatible data and
        set a rdflib grpah instance to it for writing and reading.
        """
        self.tripel_db_name_complete = self.harvester.id_in_tripel_store + COMPLETE_SUFFIX
        self.tripel_db_name = self.harvester.id_in_tripel_store
        self.error_store = self.harvester.id_in_tripel_store + ERROR_SUFFIX

        msg = u'Starting Validation'
        visitor.scribe.write(
            level='info',
            msg=msg,
        )

        unregister_logger()
        get_logger(visitor=visitor)

        validation = ValidationRun(self.tripel_db_name_complete, self.tripel_db_name, self.error_store)

        validation.run()

        # Todo: create reports
        #   store reports on harvester

        msg = u'Finished Validation'
        visitor.scribe.write(
            level='info',
            msg=msg,
        )
