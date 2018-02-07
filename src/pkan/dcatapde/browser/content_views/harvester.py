# -*- coding: utf-8 -*-
from pkan.dcatapde.api.harvester import get_all_harvester
from pkan.dcatapde.api.harvester_field_config import get_field_config
from Products.Five import BrowserView


class HarvesterOverview(BrowserView):

    def __call__(self, *args, **kwargs):
        harvester = get_all_harvester()

        self.data = []

        for harv in harvester:
            path = harv.absolute_url()
            field_config = get_field_config(harv)
            self.data.append({
                'title': harv.title,
                'path': path,
                'source_url': harv.url,
                'dry_run': path + '/dry_run',
                'real_run': path + '/real_run',
                'field_config': field_config.absolute_url(),
                'reset_fields': path + '/reset_fields',
            })

        return super(HarvesterOverview, self).__call__(*args, **kwargs)


class DryRunView(BrowserView):

    def __call__(self, *args, **kwargs):
        source = self.context.source_type(self.context)

        self.log = source.dry_run()

        return super(DryRunView, self).__call__(*args, **kwargs)


class RealRunView(BrowserView):

    def __call__(self, *args, **kwargs):
        source = self.context.source_type(self.context)

        self.log = source.real_run()

        return super(RealRunView, self).__call__(*args, **kwargs)


class ResetFieldsView(BrowserView):

    def __call__(self, *args, **kwargs):
        source = self.context.source_type(self.context)
        source.read_fields(reread=True)

        self.log = '<p>Reading fields done</p>'

        return super(ResetFieldsView, self).__call__(*args, **kwargs)
