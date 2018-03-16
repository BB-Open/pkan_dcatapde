# -*- coding: utf-8 -*-
from pkan.dcatapde.api.harvester import get_all_harvester_folder
from plone.protect.utils import addTokenToUrl
from Products.Five import BrowserView


class HarvesterListViewMixin(object):
    """
    Reusable Methods needed by all Views listing Harvester
    """

    def read_harvester_info(self, harv):

        path = harv.absolute_url()

        data = {
            'title': harv.title,
            'path': path,
            'source_url': addTokenToUrl(harv.url),
            'dry_run': addTokenToUrl(path + '/dry_run'),
            'graph_display': addTokenToUrl(path + '/graph'),
            'real_run': addTokenToUrl(path + '/real_run'),
            'reset_fields': addTokenToUrl(path + '/reset_fields'),
            'harvester_entity': addTokenToUrl(path + '/harvester_entity'),
            'edit': addTokenToUrl(path + '/edit'),
        }

        return data


class HarvesterFolderView(BrowserView, HarvesterListViewMixin):
    """
    Listing Harvester of one Folder
    """

    def __call__(self, *args, **kwargs):
        folder = self.context

        self.data = []

        for harv_id, harv in folder.contentItems():

            data = self.read_harvester_info(harv)

            self.data.append(data)

        return super(HarvesterFolderView, self).__call__(*args, **kwargs)


class HarvesterOverview(BrowserView, HarvesterListViewMixin):
    """
    Listing all Harvester Folders with included Harvester.
    """

    def __call__(self, *args, **kwargs):
        harvester_folder = get_all_harvester_folder()

        self.data = []

        for folder in harvester_folder:
            harvester = folder.contentItems()
            folder_data = []
            for harv_id, harv in harvester:
                data = self.read_harvester_info(harv)

                folder_data.append(data)
            self.data.append({
                'title': folder.title,
                'elements': folder_data,
                'path': folder.absolute_url(),
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


class EntityView(BrowserView):

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

        # harvester = get_ancestor(self.context, CT_HARVESTER)

        # harvesting_type = harvester.harvesting_type(harvester)
        #
        # used_cts = harvesting_type.get_used_cts()
        #
        # for ct in used_cts:
        #     if ct in CT_FIELD_RELATION:
        #         field = CT_FIELD_RELATION[ct]
        #         lines = copy.deepcopy(getattr(self.context, field, []))
        #         utils.set_request_annotations('pkan.vocabularies.context',
        #                                       self.context)
        #
        #         vocab = DcatFieldVocabulary(ct)
        #         options = vocab(self.context)
        #
        #         for line in lines:
        #             try:
        #                 option = options.by_value[line['dcat_field']]
        #                 line['dcat_field'] = option.title
        #             except KeyError:
        #                 continue
        #         self.data.append({
        #             'ct': ct,
        #             'lines': lines,
        #         })

        return super(EntityView, self).__call__(*args, **kwargs)
