# -*- coding: utf-8 -*-
from pkan.dcatapde import utils
from pkan.dcatapde.api.functions import get_ancestor
from pkan.dcatapde.api.harvester import get_all_harvester
from pkan.dcatapde.api.harvester_field_config import get_field_config
from pkan.dcatapde.constants import CT_HARVESTER
from pkan.dcatapde.content.harvester_field_config import CT_FIELD_RELATION
from pkan.dcatapde.vocabularies.dcat_field import DcatFieldVocabulary
from Products.Five import BrowserView

import copy


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


class FieldConfigView(BrowserView):

    def __call__(self, *args, **kwargs):
        self.base_object_url = None
        self.base_object_title = None

        if self.context.base_object:
            # fix: check why sometime to_object and sometimes not
            base_object = getattr(self.context.base_object,
                                  'to_object',
                                  self.context.base_object)
            self.base_object_title = base_object.Title()
            self.base_object_url = base_object.absolute_url()

        self.data = []

        harvester = get_ancestor(self.context, CT_HARVESTER)

        harvesting_type = harvester.harvesting_type(harvester)

        used_cts = harvesting_type.get_used_cts()

        for ct in used_cts:
            if ct in CT_FIELD_RELATION:
                field = CT_FIELD_RELATION[ct]
                lines = copy.deepcopy(getattr(self.context, field, []))
                utils.set_request_annotations('pkan.vocabularies.context',
                                              self.context)

                vocab = DcatFieldVocabulary(ct)
                options = vocab(self.context)

                for line in lines:
                    try:
                        option = options.by_value[line['dcat_field']]
                        line['dcat_field'] = option.title
                    except KeyError:
                        continue
                self.data.append({
                    'ct': ct,
                    'lines': lines,
                })

        return super(FieldConfigView, self).__call__(*args, **kwargs)
