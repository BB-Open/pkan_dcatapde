# -*- coding: utf-8 -*-
from Products.Five import BrowserView


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
