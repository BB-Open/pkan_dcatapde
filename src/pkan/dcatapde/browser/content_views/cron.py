# -*- coding: utf-8 -*-
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class RealRunCronView(BrowserView):

    def __init__(self, context, request):
        super(RealRunCronView, self).__init__(context, request)
        alsoProvides(self.request, IDisableCSRFProtection)

    def __call__(self, *args, **kwargs):
        portal = api.portal.get()
        if portal is None:
            return None
        self.log = []

        self.log.append('<h1>Harverster</h1>')

        harvester_view = getMultiAdapter((self.context, self.request),
                                         name='real_run_cron_harvest')
        harvester_view()
        self.log += harvester_view.log

        self.log.append('<h1>Transfer</h1>')

        transfer_view = getMultiAdapter((self.context, self.request),
                                        name='real_run_cron_transfer')
        transfer_view()
        self.log += transfer_view.log

        return super(RealRunCronView, self).__call__(*args, **kwargs)
