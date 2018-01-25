# -*- coding: utf-8 -*-
"""IO utilities."""

from urllib import unquote_plus
from urlparse import parse_qsl
from urlparse import urlparse


class Url(object):
    """A url object that can be compared with other url orbjects.

    It does so without regard to the vagaries of encoding, escaping,
    and ordering of parameters in query strings.
    """

    def __init__(self, url):
        parts = urlparse(url)
        _query = frozenset(parse_qsl(parts.query))
        _path = unquote_plus(parts.path)
        parts = parts._replace(query=_query, path=_path)
        self.parts = parts

    def __eq__(self, other):
        """Comparison."""
        return self.parts == other.parts

    def __hash__(self):
        """Hash."""
        return hash(self.parts)
