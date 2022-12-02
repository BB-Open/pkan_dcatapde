# -*- coding: utf-8 -*-
"""Harvesting adapter."""


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

