# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone.app.contenttypes.behaviors.collection import ICollection
from plone.app.dexterity.browser.folder_listing import FolderView


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
