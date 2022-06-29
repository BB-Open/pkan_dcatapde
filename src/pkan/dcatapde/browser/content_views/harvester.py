# -*- coding: utf-8 -*-
import gc
from datetime import datetime
from datetime import timedelta
from pkan.dcatapde import _
from pkan.dcatapde.api.functions import get_all_harvester_folder
from pkan.dcatapde.constants import CT_HARVESTER
from pkan.dcatapde.constants import CT_LGBHARVESTER
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.processors.geodata import GeodataRDFProcessor
from pkan.dcatapde.harvesting.processors.rdf2tripelstore import MultiUrlTripleStoreRDFProcessor
from pkan.dcatapde.harvesting.processors.rdf2tripelstore import TripleStoreRDFProcessor
from pkan.dcatapde.harvesting.processors.visitors import DCATVisitor
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.protect.utils import addTokenToUrl
from Products.Five import BrowserView
from pyrdf4j.errors import TerminatingError
from pytimeparse import parse
from zope.i18n import translate
from zope.interface import alsoProvides


class HarvesterListViewMixin(object):
    """
    Reusable Methods needed by all Views listing Harvester
    """

    def read_harvester_info(self, harv):

        path = harv.absolute_url()

        url = None
        if hasattr(harv, 'url'):  # noqa P002
            url = harv.url
            csw_url = None
            dcm_url = None
            complete_namespace = harv.target_namespace + '_temp'
        else:
            # special case GEO Import
            url = None
            dcm_url = harv.dcm_url
            csw_url = harv.csw_url
            complete_namespace = harv.target_namespace

        data = {
            'title': harv.title,
            'path': path,
            'source_url': url,
            'dcm': dcm_url,
            'csw': csw_url,
            'dry_run': addTokenToUrl(path + '/dry_run'),
            'real_run': addTokenToUrl(path + '/real_run'),
            'edit': addTokenToUrl(path + '/edit'),
            'clean_namespace': harv.target_namespace,
            'complete_namespace': complete_namespace,
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
    if IHarvester.providedBy(harvester):
        if harvester.url is None or harvester.url == '':
            return MultiUrlTripleStoreRDFProcessor(harvester)
        else:
            return TripleStoreRDFProcessor(harvester)
    else:
        return GeodataRDFProcessor(harvester)


class DryRunView(BrowserView):

    def __call__(self, *args, **kwargs):

        rdfproc = RDFProcessor_factory(self.context)

        visitor = DCATVisitor()
        visitor.real_run = False
        rdfproc.prepare_and_run(visitor)

        self.log = []

        # gc.get_referrers(visitor)
        # gc.get_referrers(rdfproc)

        del rdfproc
        del visitor

        gc.collect()

        self.request.response.setHeader('Cache-Control', 'no-cache, no-store')

        return super(DryRunView, self).__call__(*args, **kwargs)


class RealRunView(BrowserView):

    def __call__(self, *args, **kwargs):
        rdfproc = RDFProcessor_factory(self.context)

        visitor = DCATVisitor()
        visitor.real_run = True
        rdfproc.prepare_and_run(visitor)

        self.log = []

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
        try:
            rdfproc.prepare_and_run(visitor)
        except TerminatingError:
            del rdfproc
            del visitor
            return ['<p>Harvester fehlgeschlagen, Siehe Logs für Details</p>']

        # res = visitor.scribe.html_log()

        del rdfproc  # noqa F821
        del visitor  # noqa F821

        harv.last_run = datetime.now()
        return ['<p>Harvester fertig, Siehe Logs für Details.</p>']

    def __call__(self, *args, **kwargs):
        portal = api.portal.get()
        if portal is None:
            return None
        self.log = []

        results = api.content.find(**{'portal_type': [CT_HARVESTER, CT_LGBHARVESTER]})

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
