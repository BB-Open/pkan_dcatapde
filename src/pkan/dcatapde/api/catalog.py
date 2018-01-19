# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import CT_Catalog
from plone.api.content import create


# Add Methods
def add_catalog(context, dry_run=False, **data):
    # TODO: check if this works with new add_title
    data['title'] = data['add_title']

    if not dry_run:
        catalog = create(container=context, type=CT_Catalog, **data)

        return catalog
    else:
        return data

# Get Methods

# Delete Methods

# Related Methods
