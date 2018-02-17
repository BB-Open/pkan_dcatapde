# -*- coding: utf-8 -*-
"""Content type tests for `dcat_catalog`."""

from pkan.dcatapde import constants
from pkan.dcatapde import testing
from pkan.dcatapde.marshall.interfaces import IMarshallSource
from pkan.dcatapde.marshall.target.rdf import RDFMarshallTarget
from plone.api.content import create
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import queryMultiAdapter

import unittest


class CatalogIntegrationTest(unittest.TestCase):
    """Validate the `dcat_catalog` CT."""

    layer = testing.INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_marshall(self):
        obj = create(
            container=self.portal,
            type=constants.CT_DCAT_CATALOG,
            id='dcat_catalog_test',
        )

        target = RDFMarshallTarget()
        marshaller = queryMultiAdapter(
            (obj, target),
            interface=IMarshallSource,
        )
        marshaller.marshall()

        result = target._store.reader.graph.serialize()
        self.assertTrue('dcat_catalog_test' in result)
