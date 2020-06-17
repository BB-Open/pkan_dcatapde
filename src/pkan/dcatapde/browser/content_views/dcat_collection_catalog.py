# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from pkan.dcatapde.api.functions import get_ancestor
from pkan.dcatapde.constants import CT_DCAT_CATALOG
from pkan.dcatapde.constants import CT_DCAT_DATASET
from pkan.dcatapde.constants import CT_DCAT_DISTRIBUTION
from plone import api
from plone.app.contenttypes.behaviors.collection import ICollection
from plone.app.dexterity.browser.folder_listing import FolderView
from plone.dexterity.browser.view import DefaultView


class DcatCollectionCatalogFolderListing(FolderView):

    @property
    def collection_behavior(self):
        return ICollection(aq_inner(self.context))

    def results(self, **kwargs):
        """Return a content listing based result set with results from the
                collection query.

                :param **kwargs: Any keyword argument, which can be used for
                                catalog queries.
                :type  **kwargs: keyword argument

                :returns: plone.app.contentlisting based result set.
                :rtype: ``plone.app.contentlisting.interfaces.IContentListing``
                    based sequence.
                """
        # Extra filter
        contentFilter = dict(self.request.get('contentFilter', {}))
        contentFilter.update(kwargs.get('contentFilter', {}))
        kwargs.setdefault('custom_query', contentFilter)
        kwargs.setdefault('batch', True)
        kwargs.setdefault('b_size', self.b_size)
        kwargs.setdefault('b_start', self.b_start)

        results = self.collection_behavior.results(**kwargs)
        return results

    def get_catalog(self, obj):
        if obj.portal_type == CT_DCAT_CATALOG:
            catalog = None
        else:
            with api.env.adopt_user(username='admin'):
                catalog = get_ancestor(obj, CT_DCAT_CATALOG)
        if catalog:
            return {
                'title': catalog.Title(),
                'url': catalog.absolute_url(),
            }
        else:
            return {}

    def get_category(self, obj):
        dcat_theme = getattr(obj, 'dcat_theme', None)
        if dcat_theme:
            titles = []
            with api.env.adopt_user(username='admin'):
                for uid in dcat_theme:
                    theme = api.content.get(UID=uid)
                    titles.append(theme.Title())
            return {
                'title': ' ,'.join(titles),
            }
        else:
            return {}

    def get_license(self, obj):
        license_uid = getattr(obj, 'dct_license', None)
        if not license_uid:
            catalog = get_ancestor(obj, CT_DCAT_CATALOG)
            if catalog:
                license_uid = getattr(catalog, 'dct_license', None)
        if license_uid:
            license = api.content.get(UID=license_uid)
            if license:
                return {
                    'title': license.Title(),
                    'url': license.absolute_url(),
                }
            else:
                return {}
        else:
            return {}

    def get_formats(self, obj):
        if obj.portal_type == CT_DCAT_DATASET:
            items = obj.contentItems()
            formats = []
            for id, item in items:
                if item.portal_type == CT_DCAT_DISTRIBUTION:
                    format = getattr(item, 'dct_format', None)
                    if not format:
                        continue
                    format_obj = api.content.get(UID=format)
                    format_title = format_obj.Title()
                    formats.append(format_title)
            title = ', '.join(set(formats))
        else:
            title = ''
        if title:
            return {
                'title': title,
            }
        else:
            return {}


class DcatCollectionCatalogView(DefaultView):
    """
    Default View for DcatCollectionCatalog
    """
