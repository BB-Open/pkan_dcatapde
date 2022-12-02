# -*- coding: utf-8 -*-
"""Test vocabulary utilities."""

import unittest

from pkan.dcatapde import testing


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

    def test_query_sort_index(self):
        """Validate the `sort_on` param is still there."""
        expected = {
            'SearchableText': {'query': 'a string*'},
            'sort_on': 'sort_index',
        }
        query = {
            'criteria': [{
                'i': 'SearchableText',
                'o': 'plone.app.querystring.operation.string.contains',
                'v': 'a string*',
            }],
            'sort_on': 'sort_index',
        }

        result = self._callFUT(None, query)
        self.assertEqual(expected, result)

    def test_query_sort_order(self):
        """Validate the `sort_order` param is still there."""
        expected = {
            'SearchableText': {'query': 'a string*'},
            'sort_order': 'asc',
        }
        query = {
            'criteria': [{
                'i': 'SearchableText',
                'o': 'plone.app.querystring.operation.string.contains',
                'v': 'a string*',
            }],
            'sort_order': 'asc',
        }

        result = self._callFUT(None, query)
        self.assertEqual(expected, result)

        expected = {
            'SearchableText': {'query': 'a string*'},
            'sort_order': '1',
        }
        query = {
            'criteria': [{
                'i': 'SearchableText',
                'o': 'plone.app.querystring.operation.string.contains',
                'v': 'a string*',
            }],
            'sort_order': 1,
        }

        result = self._callFUT(None, query)
        self.assertEqual(expected, result)
