# -*- coding: utf-8 -*-
"""Utilities for vocabularies."""

from plone.app.vocabularies.utils import parseQueryString


def parse_query(context=None, query=None):
    """Parse query and transform if required."""
    parsed = {}

    if not query:
        return parsed

    if isinstance(query, basestring):
        q = query.strip()
        if len(q) <= 1:
            return parsed
        if not q.endswith('*'):
            q = '{0}*'.format(q)
        query = {
            'criteria': [{
                'i': 'SearchableText',
                'o': 'plone.app.querystring.operation.string.contains',
                'v': q,
            }],
        }

    parsed = parseQueryString(context, query['criteria'])

    if 'sort_on' in query:
        parsed['sort_on'] = query['sort_on']
    if 'sort_order' in query:
        parsed['sort_order'] = str(query['sort_order'])

    return parsed
