# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from pkan.dcatapde import _
from pkan.dcatapde.api.functions import get_all_harvester_folder
from pkan.dcatapde.constants import CT_HARVESTER
from pkan.dcatapde.harvesting.processors.rdf2tripelstore import MultiUrlTripleStoreRDFProcessor
from pkan.dcatapde.harvesting.processors.rdf2tripelstore import TripleStoreRDFProcessor
from pkan.dcatapde.harvesting.processors.visitors import DCATVisitor
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.protect.utils import addTokenToUrl
from Products.Five import BrowserView
from pytimeparse import parse
from zope.i18n import translate
from zope.interface import alsoProvides


class HarvesterListViewMixin(object):
    """
    Reusable Methods needed by all Views listing Harvester
    """

    def read_harvester_info(self, harv):

        path = harv.absolute_url()

        data = {
            'title': harv.title,
            'path': path,
            'source_url': addTokenToUrl(harv.url),
            'dry_run': addTokenToUrl(path + '/dry_run'),
            'real_run': addTokenToUrl(path + '/real_run'),
            'edit': addTokenToUrl(path + '/edit'),
            'clean_namespace': harv.target_namespace,
            'complete_namespace': harv.target_namespace + '_temp',
            'reharvesting_period': harv.reharvesting_period,
        }

        return data


class HarvesterFolderView(BrowserView, HarvesterListViewMixin):
    """
    Listing Harvester of one Folder
    """

    def __call__(self, *args, **kwargs):
        folder = self.context

        self.data = []

        for harv_id, harv in folder.contentItems():

            data = self.read_harvester_info(harv)

            self.data.append(data)

        return super(HarvesterFolderView, self).__call__(*args, **kwargs)


class HarvesterOverview(BrowserView, HarvesterListViewMixin):
    """
    Listing all Harvester Folders with included Harvester.
    """

    def __call__(self, *args, **kwargs):
        harvester_folder = get_all_harvester_folder()

        self.data = []

        for folder in harvester_folder:
            harvester = folder.contentItems()
            folder_data = []
            for harv_id, harv in harvester:
                data = self.read_harvester_info(harv)

                folder_data.append(data)
            self.data.append({
                'title': folder.title,
                'elements': folder_data,
                'path': folder.absolute_url(),
            })

        return super(HarvesterOverview, self).__call__(*args, **kwargs)


def RDFProcessor_factory(harvester):
    if harvester.url is None or harvester.url == '':
        return MultiUrlTripleStoreRDFProcessor(harvester)
    else:
        return TripleStoreRDFProcessor(harvester)


class DryRunView(BrowserView):

    def __call__(self, *args, **kwargs):

        rdfproc = RDFProcessor_factory(self.context)

        visitor = DCATVisitor()
        visitor.real_run = False
        rdfproc.prepare_and_run(visitor)

        self.log = visitor.scribe.html_log()

        del rdfproc
        del visitor
        self.request.response.setHeader('Cache-Control', 'no-cache, no-store')

        return super(DryRunView, self).__call__(*args, **kwargs)


class RealRunView(BrowserView):

    def __call__(self, *args, **kwargs):
        rdfproc = RDFProcessor_factory(self.context)

        visitor = DCATVisitor()
        visitor.real_run = True
        rdfproc.prepare_and_run(visitor)

        self.log = visitor.scribe.html_log()

        del rdfproc
        del visitor
        self.request.response.setHeader('Cache-Control', 'no-cache, no-store')

        return super(RealRunView, self).__call__(*args, **kwargs)


class RealRunCronView(BrowserView):

    def __init__(self, context, request):
        super(RealRunCronView, self).__init__(context, request)
        alsoProvides(self.request, IDisableCSRFProtection)

    def real_run(self, harv):
        rdfproc = RDFProcessor_factory(harv)

        visitor = DCATVisitor()
        visitor.real_run = True
        rdfproc.prepare_and_run(visitor)

        # res = visitor.scribe.html_log()

        del rdfproc
        del visitor

        harv.last_run = datetime.now()
        return ['<p>Harvester fertig, Siehe Logs für Details.</p>']

    def __call__(self, *args, **kwargs):
        portal = api.portal.get()
        if portal is None:
            return None
        self.log = []

        results = api.content.find(**{'portal_type': CT_HARVESTER})

        for brain in results:
            obj = brain.getObject()
            no_run_message = translate(_(u'<p>Nothing to do</p>'),
                                       context=self.request)
            self.log.append(u'<h2>{title}</h2>'.format(title=obj.title))

            if obj.reharvesting_period is None:
                self.log.append(no_run_message)
            elif obj.reharvesting_period and obj.last_run is None:
                self.log += self.real_run(obj)
            else:
                seconds = parse(obj.reharvesting_period)
                delta = timedelta(seconds=seconds)

                # noinspection PyTypeChecker
                current_delta = datetime.now() - obj.last_run

                if current_delta >= delta:
                    self.log += self.real_run(obj)
                else:
                    self.log.append(no_run_message)

        self.request.response.setHeader('Cache-Control', 'no-cache, no-store')
        return super(RealRunCronView, self).__call__(*args, **kwargs)
