# -*- coding: utf-8 -*-
"""Test vocabulary utilities."""

from pkan.dcatapde import testing

import unittest


class TestParseQuery(unittest.TestCase):
    """Validate the `parse_query` utility."""

    layer = testing.INTEGRATION_TESTING

    def _callFUT(self, context, query):
        from pkan.dcatapde.vocabularies.utils import parse_query
        return parse_query(context=context, query=query)

    def test_query_is_none(self):
        """Validate the default query."""
        result = self._callFUT(None, None)
        self.assertEqual({}, result)

    def test_query_empty_string(self):
        """Validate the query with an empty string."""
        result = self._callFUT(None, '   ')
        self.assertEqual({}, result)

    def test_query_is_basestring(self):
        """Validate the query with a basestring."""
        expected = {
            'SearchableText': {'query': 'a string*'},
        }

        result = self._callFUT(None, 'a string')
        self.assertEqual(expected, result)

        result = self._callFUT(None, '  a string   ')
        self.assertEqual(expected, result)
