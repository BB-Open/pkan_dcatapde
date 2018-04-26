# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from pkan.dcatapde import _
from pkan.dcatapde.constants import CATALOG_ADMIN_ROLE
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import PKAN_EDITOR_ROLE
from plone import api
from Products.Five import BrowserView


class LandingPageView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, *args, **kwargs):
        if api.user.is_anonymous():
            self.request.response.redirect(
                self.context.absolute_url() + '/login',
            )
            return

        self.catalog_admin = []
        self.pkan_editor = []

        portal_catalog = api.portal.get_tool('portal_catalog')
        res = portal_catalog.searchResults(
            {'portal_type': CT_DCAT_CATALOG})

        for brain in res:
            try:
                obj = brain.getObject()
            except Unauthorized:
                continue
            roles = api.user.get_roles(user=api.user.get_current(),
                                       obj=obj)
            if CATALOG_ADMIN_ROLE in roles:
                self.catalog_admin.append(obj)
            if PKAN_EDITOR_ROLE in roles:
                self.pkan_editor.append(obj)

        if not self.catalog_admin or self.pkan_editor:
            self.request.response.redirect(
                self.context.absolute_url(),
            )
            return

        return super(LandingPageView, self).__call__(*args, **kwargs)

    def catalogadmin_heading(self):
        return _('Catalogs managed as Catalog Admin')

    def pkaneditor(self):
        results = []

        for pkaneditor in self.pkan_editor:
            data = {
                'pkaneditor_name': pkaneditor.Title(),
                'path': pkaneditor.absolute_url(),
            }

            results.append(data)
        return results

    def catalogadmin(self):
        results = []

        for catalogadmin in self.catalog_admin:
            data = {
                'catalogadmin_name': catalogadmin.Title(),
                'path': catalogadmin.absolute_url(),
            }

            results.append(data)
        return results

    def display_catalogadmin(self):
        return self.catalog_admin

    def display_pkaneditor(self):
        return self.pkan_editor

    def pkaneditor_heading(self):
        return _(u'Catalogs managed as PKAN Editor')
