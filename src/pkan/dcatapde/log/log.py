# -*- coding: utf-8 -*-
from zope.i18n import translate
from zope.i18nmessageid.message import Message

import logging


class TranslatingFormatter(logging.Formatter):
    """Log formatter that translates"""

    def __init__(self, fmt=None, datefmt=None, request=None):
        """take additional request parameter"""
        self.request = request
        super(TranslatingFormatter, self).__init__(fmt, datefmt)

    def format(self, record):
        """Determine if message has to be translated"""
        if isinstance(record.msg, Message):
            # translate
            record.msg = translate(record.msg, context=self.request)
        return super(TranslatingFormatter, self).format(record)
