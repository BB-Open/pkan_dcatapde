# -*- coding: utf-8 -*-
from Products.Five import BrowserView


class DryRunView(BrowserView):

    def __call__(self, *args, **kwargs):
        source = self.context.harvesting_type(self.context)

        self.log = source.dry_run()

        return super(DryRunView, self).__call__(*args, **kwargs)
