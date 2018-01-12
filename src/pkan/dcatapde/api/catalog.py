# -*- coding: utf-8 -*-
from pkan.dcatapde.api.foafagent import add_foafagent
from pkan.dcatapde.api.functions import get_foafagent_context
from pkan.dcatapde.constants import CT_Catalog
from plone import api
from plone.api.content import create


def add_catalog(context, **data):

    publisher_info = data['new_publisher']
    choice = publisher_info.available
    name = publisher_info.name
    publisher = None
    if choice:
        publisher = api.content.get(UID=choice)
    elif name:
        publisher = add_foafagent(get_foafagent_context(),
                                  name=name,
                                  title=name)
    else:
        raise AssertionError('You must provide a publisher')

    if not publisher:
        raise AssertionError('Could not find or create Publisher')

    del data['new_publisher']

    data['title'] = data['add_title']
    data['publisher'] = publisher

    catalog = create(container=context, type=CT_Catalog, **data)

#    print(catalog.publisher)

    return catalog
