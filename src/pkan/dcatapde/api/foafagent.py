# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import CT_Foafagent
from plone.api.content import create


def add_foafagent(context, **data):
    foaf = create(container=context, type=CT_Foafagent, **data)

    return foaf
