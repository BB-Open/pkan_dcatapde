# -*- coding: utf-8 -*-
from zope.i18n import translate
from zope.i18nmessageid.message import Message

import logging


LEVEL_COLOR = {
    'INFO': 'green',
    'WARNING': 'orange',
    'ERROR': 'red',
}


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
            msg = translate(record.msg, context=self.request)
            color = LEVEL_COLOR[record.levelname]
            record.msg = u'<font color={color}>{msg}</font>'.format(
                color=color,
                msg=msg,
            )
        return super(TranslatingFormatter, self).format(record)
