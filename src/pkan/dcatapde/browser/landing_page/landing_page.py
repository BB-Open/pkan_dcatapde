# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from pkan.dcatapde import _
from pkan.dcatapde.api.functions import get_parent
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import PROVIDER_ADMIN_ROLE
from pkan.dcatapde.constants import PROVIDER_CHIEF_EDITOR_ROLE
from pkan.dcatapde.constants import PROVIDER_DATA_EDITOR_ROLE
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

        self.provider_chief_editor_obj = []
        self.provider_data_editor_obj = []
        self.provider_admin_obj = []

        self.provider_chief_editor_cat = []
        self.provider_data_editor_cat = []
        self.provider_admin_cat = []

        self.read_data()

        if not (self.provider_chief_editor_obj or
                self.provider_data_editor_obj or
                self.provider_admin_obj):
            self.request.response.redirect(
                self.context.absolute_url(),
            )
            return

        return super(LandingPageView, self).__call__(*args, **kwargs)

    def read_data(self):
        user = api.user.get_current()

        portal_catalog = api.portal.get_tool('portal_catalog')
        res = portal_catalog.searchResults(
            {'portal_type': [CT_DCAT_CATALOG, 'Folder']})

        for brain in res:
            try:
                obj = brain.getObject()
            except Unauthorized:
                continue
            roles = api.user.get_roles(user=user,
                                       obj=obj)
            roles_parent = api.user.get_roles(user=user,
                                              obj=get_parent(obj))
            if PROVIDER_CHIEF_EDITOR_ROLE in roles and \
                    PROVIDER_CHIEF_EDITOR_ROLE not in roles_parent:
                self.provider_chief_editor_obj.append(obj)
            elif PROVIDER_CHIEF_EDITOR_ROLE in roles and \
                    obj.portal_type == CT_DCAT_CATALOG:
                self.provider_chief_editor_cat.append(obj)
            if PROVIDER_DATA_EDITOR_ROLE in roles and \
                    PROVIDER_DATA_EDITOR_ROLE not in roles_parent:
                self.provider_data_editor_obj.append(obj)
            elif PROVIDER_DATA_EDITOR_ROLE in roles and \
                    obj.portal_type == CT_DCAT_CATALOG:
                self.provider_data_editor_cat.append(obj)
            if PROVIDER_ADMIN_ROLE in roles and \
                    PROVIDER_ADMIN_ROLE not in roles_parent:
                self.provider_admin_obj.append(obj)
            elif PROVIDER_ADMIN_ROLE in roles and \
                    obj.portal_type == CT_DCAT_CATALOG:
                self.provider_admin_cat.append(obj)

    def providerchiefeditor_heading(self):
        return _(u'Folders and Catalogs managed as Provider Chief Editor')

    def providerdataeditor(self):
        results = []

        for providerdataeditor in self.provider_data_editor_obj:
            data = {
                'providerdataeditor_name': providerdataeditor.Title(),
                'path': providerdataeditor.absolute_url(),
            }

            results.append(data)
        return results

    def provideradmin(self):
        results = []

        for provideradmin in self.provider_admin_obj:
            data = {
                'provideradmin_name': provideradmin.Title(),
                'path': provideradmin.absolute_url(),
            }

            results.append(data)
        return results

    def providerchiefeditor(self):
        results = []

        for providerchiefeditor in self.provider_chief_editor_obj:
            data = {
                'providerchiefeditor_name': providerchiefeditor.Title(),
                'path': providerchiefeditor.absolute_url(),
            }

            results.append(data)
        return results

    def providerdataeditor_cat(self):
        results = []

        for providerdataeditor in self.provider_data_editor_cat:
            data = {
                'providerdataeditor_name': providerdataeditor.Title(),
                'path': providerdataeditor.absolute_url(),
            }

            results.append(data)
        return results

    def provideradmin_cat(self):
        results = []

        for provideradmin in self.provider_admin_cat:
            data = {
                'provideradmin_name': provideradmin.Title(),
                'path': provideradmin.absolute_url(),
            }

            results.append(data)
        return results

    def providerchiefeditor_cat(self):
        results = []

        for providerchiefeditor in self.provider_chief_editor_cat:
            data = {
                'providerchiefeditor_name': providerchiefeditor.Title(),
                'path': providerchiefeditor.absolute_url(),
            }

            results.append(data)
        return results

    def display_providerchiefeditor(self):
        return self.provider_chief_editor_obj

    def display_providerdataeditor(self):
        return self.provider_data_editor_obj

    def providerdataeditor_heading(self):
        return _(u'Folders and Catalogs managed as Provider Data Editor')

    def display_provideradmin(self):
        return self.provider_admin_obj

    def provideradmin_heading(self):
        return _(u'Folders managed as Provider Admin')
