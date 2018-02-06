# -*- coding: utf-8 -*-
"""Testing utils."""

import itertools
import os
import re
import responses
import urllib


HOST = 'demoapi.com'
BASE_URL = 'https://{0}'.format(HOST)
BASE_PARAMS = {}


def setup_fixtures():
    """Setup the test fixtures for integration tests."""
    _register(
        'licenses/licenses.rdf',
        fixture='licenses.rdf',
    )


def join_url(url, *paths):
    """Join individual URL strings together, and returns a single string.

    Usage::

        >>> join_url('example.com', 'index.html')
        'example.com/index.html'
    """
    for path in paths:
        url = re.sub(r'/?$', re.sub(r'^/?', '/', path), url)
    return url


def load_fixture(name, path=None):
    """Return a file-like fixture, just like urlopen would."""
    if path is None:
        path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'fixtures',
        )
    fixture = open(os.path.join(path, name), 'r')
    return fixture.read()


def get_url(base_url, endpoint):
    """Return the endpoint URL."""
    return '/'.join([
        base_url,
        endpoint,
    ])


def _register(
    endpoint,
    content=None,
    path=None,
    fixture=None,
    content_type=None,
    params=None,
):
    if fixture:
        content = load_fixture(fixture, path=path)
    base_url = get_url(BASE_URL, endpoint)
    if not content_type:
        content_type = 'application/rdf+xml'
    if not params:
        responses.add(
            responses.GET,
            re.compile(base_url),
            body=content,
            match_querystring=True,
            status=200,
            content_type=content_type,
        )
    else:
        for keys in itertools.permutations(params.keys()):
            query = urllib.urlencode([
                (key, params.get(key)) for key in keys
            ])
            responses.add(
                responses.GET,
                re.compile('\?'.join((base_url, query))),
                body=content,
                match_querystring=True,
                status=200,
                content_type=content_type,
            )
