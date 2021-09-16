# -*- coding: utf-8 -*-
# from pkan.blazegraph.api import tripel_store
# from pkan.blazegraph.errors import HarvestURINotReachable
import sys

from Products.Five import BrowserView
from pkan.dcatapde import _
from pkan.dcatapde.api.functions import get_all_transfer_folder
from pkan.dcatapde.constants import ADMIN_USER, ADMIN_PASS, RDF4J_BASE
from pkan.dcatapde.constants import CT_TRANSFER, RDF_REPO_TYPE
from pkan.dcatapde.harvesting.processors.transfer import RDFProcessorTransfer
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.protect.utils import addTokenToUrl
from pyrdf4j.errors import URINotReachable
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth
from requests.exceptions import SSLError
from zope.i18n import translate
from zope.interface import alsoProvides


class TransferListViewMixin(object):
    """
    Reusable Methods needed by all Views listing Transfer
    """

    def read_transfer_info(self, trans):

        path = trans.absolute_url()

        data = {
            'path': path,
            'title': trans.title,
            'source_url': addTokenToUrl(trans.url),
            'real_run': addTokenToUrl(path + '/real_run_transfer'),
            'edit': addTokenToUrl(path + '/edit'),
            'target_namespace': trans.target_namespace,
            'source_namespace': trans.source_namespace,
            'is_enabled': trans.is_enabled,
        }

        return data


class TransferFolderView(BrowserView, TransferListViewMixin):
    """
    Listing Transfer of one Folder
    """

    def __call__(self, *args, **kwargs):
        folder = self.context

        self.data = []

        for trans_id, trans in folder.contentItems():

            data = self.read_transfer_info(trans)

            self.data.append(data)

        return super(TransferFolderView, self).__call__(*args, **kwargs)


class TransferOverview(BrowserView, TransferListViewMixin):
    """
    Listing all Transfer Folders with included Transfer.
    """

    def __call__(self, *args, **kwargs):
        transfer_folder = get_all_transfer_folder()

        self.data = []

        for folder in transfer_folder:
            transfer = folder.contentItems()
            folder_data = []
            for trans_id, trans in transfer:
                data = self.read_transfer_info(trans)

                folder_data.append(data)
            self.data.append({
                'title': folder.title,
                'elements': folder_data,
                'path': folder.absolute_url(),
            })

        return super(TransferOverview, self).__call__(*args, **kwargs)


def RDFProcessor_factory(transfer, raise_exceptions=False):
    return RDFProcessorTransfer(transfer, raise_exceptions=raise_exceptions)


class RealRunView(BrowserView):

    def __call__(self, *args, **kwargs):
        rdfproc = RDFProcessor_factory(self.context)
        self.log = []
        try:
            response = rdfproc.real_run()
            text = 'Database Response: '
            text = text + response.replace('<', '&lt;').replace('>', '&gt;')

            self.log.append(text)
        except URINotReachable:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            msg = u"GET termiated due to error %s %s" % (exc_type, exc_value)
            self.log.append('<p>URL not reachable. Skipping.</p>')
            self.log.append('<p>' + msg + '</p>')

        return super(RealRunView, self).__call__(*args, **kwargs)


class RealRunCronView(BrowserView):

    def __init__(self, context, request):
        super(RealRunCronView, self).__init__(context, request)
        alsoProvides(self.request, IDisableCSRFProtection)
        self.rdf4j = RDF4J(rdf4j_base=RDF4J_BASE)
        self.auth = HTTPBasicAuth(ADMIN_USER, ADMIN_PASS)

    def real_run(self, trans):
        rdfproc = RDFProcessor_factory(trans)
        try:
            response = rdfproc.real_run()
            text = 'Database Response: '
            text = text + \
                response.replace('<', '&lt;').replace('>', '&gt;')
        except SSLError:
            text = 'Database not reachable.'

        return [text]

    def __call__(self, *args, **kwargs):
        portal = api.portal.get()
        if portal is None:
            return None
        self.log = []

        results = api.content.find(**{'portal_type': CT_TRANSFER})
        target_namespaces = []
        url_transfers = []
        name_space_transfers = []

        for brain in results:
            obj = brain.getObject()

            if not obj.is_enabled:
                no_run_message = translate(_(u'<p>Nothing to do</p>'),
                                           context=self.request)
                self.log.append(u'<h2>{title}</h2>'.format(title=obj.title))
                self.log.append(no_run_message)
            else:
                target = obj.id_in_tripel_store
                if target not in target_namespaces:
                    target_namespaces.append(target)
                if obj.url:
                    url_transfers.append(obj)
                elif obj.source_namespace:
                    name_space_transfers.append(obj)

        for namespace in target_namespaces:
            self.log.append(
                u'<h2>Clear Namespace {title} and create if not exists</h2>'.format(title=namespace))
            self.rdf4j.create_repository(namespace, repo_type=RDF_REPO_TYPE, overwrite=False, accept_existing=True, auth=self.auth)
            self.rdf4j.empty_repository(namespace, auth=self.auth)
            self.log.append(u'<p>Erledigt</p>')
        for obj in url_transfers:
            self.log.append(
                u'<h2>URL Transfer: {title}</h2>'.format(title=obj.title))
            try:
                self.log += self.real_run(obj)
            except URINotReachable:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                msg = u"GET termiated due to error %s %s" % (exc_type, exc_value)
                self.log.append('<p>URL not reachable. Skipping.</p>')
                self.log.append('<p>' + msg + '</p>')
        for obj in name_space_transfers:
            self.log.append(
                u'<h2>Namespace Transfer: {title}</h2>'.format(
                    title=obj.title))
            self.log += self.real_run(obj)

        return super(RealRunCronView, self).__call__(*args, **kwargs)
