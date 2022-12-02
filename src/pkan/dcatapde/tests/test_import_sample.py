# -*- coding: utf-8 -*-
"""Sample Test."""

import unittest

import requests

from pkan.dcatapde import testing
from pkan.dcatapde.tests import utils


class TestImport(unittest.TestCase):
    """Validate import."""

    layer = testing.FUNCTIONAL_TESTING

    def test_foo(self):
        """Test import."""
        req = requests.get(utils.BASE_URL + '/licenses/licenses.rdf')
        self.assertEqual(req.status_code, 200)
