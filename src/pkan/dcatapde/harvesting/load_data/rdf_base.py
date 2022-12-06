# -*- coding: utf-8 -*-
"""Harvesting adapter."""
from pkan.dcatapde import _
from pkan.dcatapde.constants import CONTRIBUTER_ID


class BaseRDFProcessor(object):
    """Generic RDF Processor. Works for JSONLD, XML and Turtle RDF sources"""

    raise_exceptions = True

    struct_class = None             # Todo: Is this useful
    harvesting_context = None       # Todo: Is this useful

    def __init__(self, harvester):
        self.harvester = harvester
        self.setup_logger()
        # self.literal_handler = LiteralHandler()

    def setup_logger(self):
        """Log to a io.stream that can later be embedded in the view output"""
        pass

    def prepare_and_run(self, visitor):
        pass


    def add_contributer_id(self, visitor, rdf4j, auth, dbs):
        msg = _(u'Add Contributer IDs')
        visitor.scribe.write(
            level='info',
            msg=msg,
        )
        for db in dbs:
            msg = _(u'Working on {database}')
            visitor.scribe.write(
                level='info',
                msg=msg,
                database=db,
            )
            prepared_query = """prefix dcat: <http://www.w3.org/ns/dcat#>
                                SELECT DISTINCT ?id WHERE {?id a dcat:Dataset .}"""
            response = rdf4j.query_repository(db, prepared_query, auth=auth)
            res = response['results']['bindings']
            for obj in res:
                INSERT = """
                prefix dcatde: <http://dcat-ap.de/def/dcatde/>
                <{s}> {p} <{o}> ."""
                insert = INSERT.format(
                    s=obj['id']['value'],
                    p='dcatde:contributorID',
                    o=CONTRIBUTER_ID,
                )
                rdf4j.add_data_to_repo(
                    db,
                    insert.encode('utf-8'),
                    'text/turtle',
                    auth=auth,
                )
            msg = _(u'Finished {database}')
            visitor.scribe.write(
                level='info',
                msg=msg,
                database=db,
            )

