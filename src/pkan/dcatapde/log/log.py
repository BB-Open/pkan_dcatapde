# -*- coding: utf-8 -*-
import logging

from zope.i18n import translate
from zope.i18nmessageid.message import Message

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
            link = u'<a class="context pat-plone-modal" ' \
                   u'target="_blank" href="{uri}">Modify</a>'
            color = LEVEL_COLOR[record.levelname]
            color_msg = u'<font color={color}>{msg}</font><div>{link}</div>'
            record.msg = color_msg.format(
                color=color,
                msg=msg,
                link=link.format(
                    uri=u'http://localhost:8080/Plone6/harvester_preview',
                ),
            )
        return super(TranslatingFormatter, self).format(record)
