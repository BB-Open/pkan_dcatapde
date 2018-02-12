# -*- coding: utf-8 -*-

from pkan.dcatapde.content.base import IDCAT


class ExportActionOnDCAT(object):
    """Is called by actions (see actions.xml) to determine if they should be
    shown are not."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def active(self):
        return IDCAT.providedBy(self.context)
