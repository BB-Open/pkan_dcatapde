from pkan.dcatapde.api.functions import get_foafagent_context, get_obj_by_path
from pkan.dcatapde.api.foafagent import add_foafagent
from pkan.dcatapde.constants import CT_Catalog
from plone.dexterity.utils import createContentInContainer


def add_catalog(context, **data):

    publisher_info = data['new_publisher']
    choice = publisher_info.available
    name = publisher_info.name
    publisher = None
    if choice:
        publisher = get_obj_by_path(choice)
    elif name:
        publisher = add_foafagent(get_foafagent_context(), name=name, title=name)
    else:
        raise AssertionError("You must provide a publisher")

    if not publisher:
        raise AssertionError("Could not find or create Publisher")

    del data['new_publisher']

    data['title'] = data['add_title']
    data['publisher'] = publisher

    catalog = createContentInContainer(context,
                                       CT_Catalog,
                                       **data)

    print catalog.publisher

    return catalog