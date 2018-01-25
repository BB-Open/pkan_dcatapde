
# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import CT_Catalog, CT_DctLicenseDocument
from plone.api.content import create


# Add Methods
def add_dct_licensedocument(context, dry_run=False, **data):

    if not dry_run:
        result = create(container=context, type=CT_DctLicenseDocument, **data)

        return result
    else:
        return data

# Get Methods

# Delete Methods

# Related Methods
