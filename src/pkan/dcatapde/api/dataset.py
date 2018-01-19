# Add Methods
from pkan.dcatapde.constants import CT_Dataset
from plone.api.content import create


def add_dataset(context, dry_run=False, **data):
    if not dry_run:
        dataset = create(container=context, type=CT_Dataset, **data)

        return dataset
    else:
        return data

# Get Methods

# Delete Methods

# Related Methods
