# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import FIELDSET_ORDER_AT_END
from plone.dexterity.browser.view import DefaultView
from Products.CMFCore.interfaces import IFolderish


class PKANDefaultView(DefaultView):
    """
    View for all Pkan-Types.
    """
    @property
    def fieldset_order_end(self):
        return FIELDSET_ORDER_AT_END

    def display_folder_listing(self):
        return IFolderish.providedBy(self.context)

    def __call__(self, *args, **kwargs):
        self.groups_at_end = ()
        super(PKANDefaultView, self).__call__(*args, **kwargs)

        # filter fields for not logged in user
        groups, groups_at_end = self.filtered_groups()
        # just sort fieldsets for logged in user

        self.groups = tuple(groups)
        self.groups_at_end = tuple(groups_at_end)

        return self.render()

    def filtered_groups(self):
        groups = []
        groups_at_end = []
        # filter empty fields
        # use self.w holding all widgets because iterating over
        # self.widgets still display some empty fields
        for x in list(self.w.keys()):
            value = getattr(self.context, x, None)
            if not value:
                try:
                    del self.widgets[x]
                    del self.w[x]
                except KeyError:
                    pass

        # filter empty groups
        for group_name in list(self.fieldsets.keys()):
            group = self.fieldsets[group_name]
            group_is_empty = True

            # filter empty fields in group

            # use self.w holding all widgets because iterating over
            # group.widgets still display some empty fields
            for x in list(self.w.keys()):
                if x in group.widgets:
                    value = getattr(self.context, x, None)
                    if not value:
                        del group.widgets[x]
                        del self.w[x]
                    else:
                        group_is_empty = False

            if not group_is_empty:
                if group_name in self.fieldset_order_end:
                    groups_at_end.append(group)
                else:
                    groups.append(group)
            else:
                del self.fieldsets[group_name]

        return groups, groups_at_end


class PublisherCardDefaultView(DefaultView):
    """
    View for Publisher Card
    """
