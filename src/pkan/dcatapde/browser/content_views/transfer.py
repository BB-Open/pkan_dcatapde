# -*- coding: utf-8 -*-
from pkan.blazegraph.api import tripel_store
from pkan.dcatapde import _
from pkan.dcatapde.api.functions import get_all_transfer_folder
from pkan.dcatapde.constants import CT_TRANSFER
from pkan.dcatapde.harvesting.rdf.transfer import RDFProcessorTransfer
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.protect.utils import addTokenToUrl
from Products.Five import BrowserView
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

        response = rdfproc.real_run()

        text = 'Database Response: '
        text = text + response.text.replace('<', '&lt;').replace('>', '&gt;')

        self.log = [text]

        return super(RealRunView, self).__call__(*args, **kwargs)


class RealRunCronView(BrowserView):

    def __init__(self, context, request):
        super(RealRunCronView, self).__init__(context, request)
        alsoProvides(self.request, IDisableCSRFProtection)

    def real_run(self, trans):
        rdfproc = RDFProcessor_factory(trans)
        try:
            response = rdfproc.real_run()
            text = 'Database Response: '
            text = text + \
                response.text.replace('<', '&lt;').replace('>', '&gt;')
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

            if obj.reharvesting_period is None:
                no_run_message = translate(_(u'<p>Nothing to do</p>'),
                                           context=self.request)
                self.log.append(u'<h2>{title}</h2>'.format(title=obj.title))
                self.log.append(no_run_message)
            # cause we empty, we have to rerun all
            # elif obj.reharvesting_period and obj.last_run is None:
            #     self.log += self.real_run(obj)
            else:
                target_namespaces.append(obj.id_in_tripel_store())
                if obj.url:
                    url_transfers.append(obj)
                elif obj.source_namespace:
                    name_space_transfers.append(obj)

        for namespace in target_namespaces:
            self.log.append(
                u'<h2>Clear Namespace {title}</h2>'.format(title=namespace))
            tripel_store.empty_namespace(namespace)
            self.log.append(u'<p>Erledigt</p>')
        for obj in url_transfers:
            self.log.append(
                u'<h2>URL Transfer: {title}</h2>'.format(title=obj.title))
            self.log += self.real_run(obj)
        for obj in name_space_transfers:
            self.log.append(
                u'<h2>Namespace Transfer: {title}</h2>'.format(
                    title=obj.title))
            self.log += self.real_run(obj)

        return super(RealRunCronView, self).__call__(*args, **kwargs)
