# -*- coding: utf-8 -*-
"""Remembering things"""
from datetime import datetime


class Scribe(object):
    """Instance to write things to and to retrieve them later"""

    def __init__(self):
        self.data = []

    def write(self, msg=None, level=None, **data):
        self.data.append({
            'time': datetime.now(),
            'log': msg,
            'level': level,
            'data': data,
        })

    def read(self):
        for entry in self.data:
            try:
                msg = entry['log'].format(
                    time=entry['time'],
                    level=entry['level'],
                    **entry['data'])
            except KeyError:
                pass
            yield {'msg': msg, 'data': entry['data']}
