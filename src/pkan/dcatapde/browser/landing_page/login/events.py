# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import LANDING_PAGE_VIEW
from zope.component.hooks import getSite


def userLogin(obj, event):
    """Redirects logged in users to personal dashboard"""

    # get portal object
    portal = getSite()

    # check if we have an access to request object
    request = getattr(portal, 'REQUEST', None)
    if not request:
        return

    # determine the appropriate destination
    url = portal.absolute_url()
    # check if came_from is not empty, then clear it up, otherwise further
    # Plone scripts will override our redirect
    if request.get('came_from'):
        request['came_from'] = ''
        request.form['came_from'] = ''
    request.RESPONSE.redirect(url + '/' + LANDING_PAGE_VIEW)
