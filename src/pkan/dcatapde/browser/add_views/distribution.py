# -*- coding: utf-8 -*-
"""Add view for DCATAP-DE content."""


from pkan.dcatapde.browser.add_views.default_add_view import PkanDefaultAddForm
from pkan.dcatapde.browser.add_views.default_add_view import PkanDefaultAddView


class DistributionAddForm(PkanDefaultAddForm):
    """Default add form."""

    def create(self, data):
        try:
            local_file_obj = data['local_file']
        except KeyError:
            return super(DistributionAddForm, self).create(data)

        if local_file_obj is not None:
            download_postfix = '/@@download/local_file'
            data['dcat_downloadURL'] = self.context.absolute_url() \
                + download_postfix
        return super(DistributionAddForm, self).create(data)


class DistributionAddView(PkanDefaultAddView):
    """Default add view."""

    form = DistributionAddForm
