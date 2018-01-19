# Add Methods
from plone.api.content import create

from pkan.dcatapde.constants import CT_Distribution


def add_distribution(context, dry_run=False, **data):
    if not dry_run:
        dist = create(container=context, type=CT_Distribution, **data)

        return dist
    else:
        return data

# Get Methods

# Delete Methods

# Related Methods