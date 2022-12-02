# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from Products.Five import BrowserView
from plone import api
from zope.i18n import translate

from pkan.dcatapde import _
from pkan.dcatapde.api.functions import get_parent
from pkan.dcatapde.api.functions import is_admin
from pkan.dcatapde.constants import ADMIN_LANDING_PAGE
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import PROVIDER_ADMIN_ROLE
from pkan.dcatapde.constants import PROVIDER_CHIEF_EDITOR_ROLE
from pkan.dcatapde.constants import PROVIDER_DATA_EDITOR_ROLE
from pkan.dcatapde.constants import SIZE_FACTOR
from pkan.dcatapde.constants import SIZE_ROUND
from pkan.dcatapde.constants import SIZE_UNIT
from pkan.dcatapde.constants import VOLUMN_TYPES
from pkan.dcatapde.i18n import LABEL_SUM
from pkan.dcatapde.i18n import VOLUMN_RESULT_STRING


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

        if is_admin():
            self.request.response.redirect(
                self.context.absolute_url() + '/' + ADMIN_LANDING_PAGE,
            )
            return

        self.chief_editor_obj = []
        self.data_editor_obj = []
        self.admin_obj = []

        self.provider_chief_editor_cat = []
        self.provider_data_editor_cat = []
        self.provider_admin_cat = []

        self.read_data()

        check = self.chief_editor_obj or self.data_editor_obj or self.admin_obj

        if not check:
            self.request.response.redirect(
                self.context.absolute_url(),
            )
            return

        return super(LandingPageView, self).__call__(*args, **kwargs)

    def read_data(self):
        user = api.user.get_current()

        res = api.content.find(context=None,
                               portal_type=[CT_DCAT_CATALOG, 'Folder'])

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
                self.chief_editor_obj.append(obj)
            elif PROVIDER_CHIEF_EDITOR_ROLE in roles and \
                    obj.portal_type == CT_DCAT_CATALOG:
                self.provider_chief_editor_cat.append(obj)
            if PROVIDER_DATA_EDITOR_ROLE in roles and \
                    PROVIDER_DATA_EDITOR_ROLE not in roles_parent:
                self.data_editor_obj.append(obj)
            elif PROVIDER_DATA_EDITOR_ROLE in roles and \
                    obj.portal_type == CT_DCAT_CATALOG:
                self.provider_data_editor_cat.append(obj)
            if PROVIDER_ADMIN_ROLE in roles and \
                    PROVIDER_ADMIN_ROLE not in roles_parent:
                self.admin_obj.append(obj)
            elif PROVIDER_ADMIN_ROLE in roles and \
                    obj.portal_type == CT_DCAT_CATALOG:
                self.provider_admin_cat.append(obj)

    def providerchiefeditor_heading(self):
        return _(u'Folders and Catalogs managed as Provider Chief Editor')

    def providerdataeditor(self):
        results = []

        for providerdataeditor in self.data_editor_obj:
            data = {
                'providerdataeditor_name': providerdataeditor.Title(),
                'path': providerdataeditor.absolute_url(),
            }
            data.update(self.stat(providerdataeditor))

            results.append(data)
        return results

    def provideradmin(self):
        results = []

        for provideradmin in self.admin_obj:
            data = {
                'provideradmin_name': provideradmin.Title(),
                'path': provideradmin.absolute_url(),
            }
            data.update(self.stat(provideradmin))

            results.append(data)
        return results

    def providerchiefeditor(self):
        results = []

        for providerchiefeditor in self.chief_editor_obj:
            data = {
                'providerchiefeditor_name': providerchiefeditor.Title(),
                'path': providerchiefeditor.absolute_url(),
            }
            data.update(self.stat(providerchiefeditor))

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
        return self.chief_editor_obj

    def display_providerdataeditor(self):
        return self.data_editor_obj

    def providerdataeditor_heading(self):
        return _(u'Folders and Catalogs managed as Provider Data Editor')

    def display_provideradmin(self):
        return self.admin_obj

    def provideradmin_heading(self):
        return _(u'Folders managed as Provider Admin')

    def stat(self, context):
        portal_types = VOLUMN_TYPES.keys()
        folder_path = '/'.join(context.getPhysicalPath())
        data = []
        size_all = 0.0
        count_all = 0
        for portal_type in portal_types:
            results = api.content.find(**{'portal_type': portal_type,
                                          'path': folder_path})
            count = len(results)
            size = 0
            for brain in results:
                obj = brain.getObject()
                res = obj
                for element in VOLUMN_TYPES[portal_type]:
                    res = getattr(res, element, None)
                if res:
                    size += res
            if size:
                data.append(
                    _(VOLUMN_RESULT_STRING, mapping={
                        'label': translate(portal_type, context=self.request),
                        'size': round(float(size) / float(SIZE_FACTOR),
                                      SIZE_ROUND),
                        'count': count,
                        'unit': SIZE_UNIT,
                    }),
                )

                size_all += size
                count_all += count
        if size_all:
            data.append(
                _(VOLUMN_RESULT_STRING, mapping={
                    'label': LABEL_SUM,
                    'size': round(float(size_all) / float(SIZE_FACTOR),
                                  SIZE_ROUND),
                    'count': count_all,
                    'unit': SIZE_UNIT,
                }),
            )

        return {'load_data': data}


class AdminLandingPageView(LandingPageView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, *args, **kwargs):

        self.data = self.read_data()

        return super(LandingPageView, self).__call__(*args, **kwargs)

    def read_data(self, context=None, current_depth=0):
        if current_depth > 2:
            return None
        current_depth = current_depth + 1

        if not context:
            context = self.context

        result_data = []
        for id, obj in context.contentItems():
            if obj.portal_type != 'Folder':
                continue
            if obj == context:
                continue
            stat = self.stat(obj)
            if not stat['load_data']:
                continue
            sub_elements = self.read_data(obj, current_depth=current_depth)

            data = {
                'title': obj.Title(),
                'url': obj.absolute_url(),
                'stat': stat,
                'sub_elements': sub_elements,
            }

            result_data.append(data)
        return result_data
