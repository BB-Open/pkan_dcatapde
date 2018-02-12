# -*- coding: utf-8 -*-
"""Preprocessor Adapter."""
from pkan.dcatapde import constants as c
from pkan.dcatapde.content.harvester import IHarvester
from pkan.dcatapde.harvesting.data_type.interfaces import IPotsdam
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces import IRequest


@adapter(IHarvester, IRequest)
@implementer(IPotsdam)
class Potsdam(object):
    """Potsdam Preprocessor."""

    def __init__(self, harvester):
        self.harvester = harvester
        self.url_prefix = 'https://opendata.potsdam.de/explore/dataset/'

    def clean_data(self, data_manager):

        if c.CT_DCAT_DATASET in data_manager.data:
            self.clean_dataset(data_manager)

        if c.CT_DCAT_DISTRIBUTION in data_manager.data:
            self.clean_distribution(data_manager)

    def clean_dataset(self, data_manager):
        for id in data_manager.ids:
            title = 'Dataset {x}'.format(
                x=data_manager.ids.index(id),
            )
            data_manager.reset_attribute(
                c.CT_DCAT_DATASET,
                id,
                'title',
                payload=title,
            )

#            rdf_about = data_manager.get_data_for_field(c.CT_DCAT_DATASET,
#                                                        id,
#                                                        'rdf_about')
#            if rdf_about :
#                url = str(rdf_about.payload)
#                try:
#                    URI().validate(url)
#                except InvalidURI:
#                    url = self.url_prefix + url
#            else:
#                url = self.url_prefix + url
#
#            rdf_about.payload = url

            title_foaf_agent = 'Agent {x}'.format(
                x=data_manager.ids.index(id),
            )

            data_manager.reset_attribute(
                c.CT_DCAT_DATASET + ':dct_publisher:' + c.CT_FOAF_AGENT,
                id,
                'title',
                payload=title_foaf_agent,
            )
#            data_manager.reset_attribute(
#                c.CT_DCAT_DATASET + ':dct_publisher:' + c.CT_FOAF_AGENT,
#                id,
#                'rdf_about',
#                payload=url,
#            )

    def clean_distribution(self, data_manager):
        for id in data_manager.ids:
            title = 'Distribution {x}'.format(
                x=data_manager.ids.index(id),
            )
            data_manager.reset_attribute(
                c.CT_DCAT_DISTRIBUTION,
                id,
                'title',
                payload=title,
            )
