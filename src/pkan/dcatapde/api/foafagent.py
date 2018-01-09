from pkan.dcatapde.constants import CT_Foafagent
from plone.dexterity.utils import createContentInContainer


def add_foafagent(context, **data):
    foaf = createContentInContainer(context,
                                       CT_Foafagent,
                                       **data)

    return foaf