import tempfile
from datetime import datetime

import transaction
from pkan_config.config import get_config
from plone.namedfile.file import NamedBlobFile
from pyrdf4j.errors import QueryFailed
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth
from shacl.constants import NUMBER_OF_QUERY
from shacl.log.log import unregister_logger, get_logger
from shacl.report import PDFBlockReport
from shacl.validate import ValidationRun

from pkan.dcatapde.constants import ERROR_SUFFIX, COMPLETE_SUFFIX, COMPARISON_FIELDS
from pkan.dcatapde.harvesting.load_data.rdf_base import BaseRDFProcessor


class TripleStoreRDFValidator(BaseRDFProcessor):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    def prepare_and_run(self, visitor):
        """Validate Complete Store.
        Store validated data on target store.
        Store Errors on error Store.
        Generate report.
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

        del validation

        msg = u'Creating Report'
        visitor.scribe.write(
            level='info',
            msg=msg
        )

        report_file = tempfile.NamedTemporaryFile(suffix='.pdf')

        comparison_fields = []

        cfg = get_config()
        self.rdf4j = RDF4J(rdf4j_base=cfg.RDF4J_BASE)
        self.auth = HTTPBasicAuth(cfg.ADMIN_USER, cfg.ADMIN_PASS)

        for field, short_query in COMPARISON_FIELDS.items():
            query = NUMBER_OF_QUERY.format(short_query)
            try:
                old = self.rdf4j.query_repository(self.tripel_db_name_complete, query=query, auth=self.auth)
                new = self.rdf4j.query_repository(self.tripel_db_name, query=query, auth=self.auth)
            except QueryFailed:
                continue
            comparison_fields.append({
                'field': field,
                'old': old['results']['bindings'][0]['count']['value'],
                'new': new['results']['bindings'][0]['count']['value']
            })

        provider = self.harvester.title
        date = datetime.now()
        date_formatted = date.strftime('%Y-%m-%d %H:%M')
        title = self.harvester.id_in_tripel_store

        PDFBlockReport().generate(self.error_store, report_file.name, display_details=True, provider=provider,
                                  date=date_formatted, comparison_fields=comparison_fields, title=title)

        date_formatted_file = date.strftime('%Y_%m_%d_%H:%M')

        blob_file = NamedBlobFile(data=report_file.read(),
                                  filename=self.tripel_db_name + '_' + date_formatted_file + '_report.pdf',
                                  contentType='application/pdf')

        self.harvester.pdf_report = blob_file

        report_file.close()

        # Todo: create reports
        #   store reports on harvester
        msg = u'Setting Last Run to now.'
        visitor.scribe.write(
            level='info',
            msg=msg, )

        self.harvester.last_run = date

        transaction.commit()

        msg = u'Finished Validation'
        visitor.scribe.write(
            level='info',
            msg=msg,
        )
