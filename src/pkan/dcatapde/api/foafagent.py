# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import CT_Foafagent
from plone import api


def add_foafagent(context, dry_run=False, **data):
    if not dry_run:
        foaf = api.content.create(container=context, type=CT_Foafagent, **data)

        return foaf


def get_foafagent_context():
    # todo context should not be the site
    context = api.portal.get()
    return context