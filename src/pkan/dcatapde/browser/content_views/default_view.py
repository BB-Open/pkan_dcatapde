# -*- coding: utf-8 -*-
from plone.dexterity.browser.view import DefaultView
from Products.CMFCore.interfaces import IFolderish


class PKANDefaultView(DefaultView):
    """
    View for all Pkan-Types.
    """

    def display_folder_listing(self):
        return IFolderish.providedBy(self.context)
