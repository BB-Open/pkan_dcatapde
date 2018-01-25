# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import CT_DctMediatypeorextent
from plone.api.content import create


# Add Methods
def add_dct_mediatypeorextent(context, dry_run=False, **data):

    if not dry_run:
        result = create(container=context, type=CT_DctMediatypeorextent, **data)

        return result
    else:
        return data

# Get Methods

# Delete Methods

# Related Methods