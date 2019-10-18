# -*- coding: utf-8 -*-
from pkan.dcatapde.constants import IMPRESSUM
from plone import api
from Products.CMFPlone.browser.contact_info import ContactForm
from Products.Five import BrowserView


class RedirectImpressumIfExists(BrowserView):

    def __call__(self, *args, **kwargs):
        impressum = api.content.find(Title=IMPRESSUM)

        if impressum:
            self.request.response.redirect(
                impressum[0].getObject().absolute_url(),
            )
            return
        else:
            return super(RedirectImpressumIfExists, self).__call__(*args,
                                                                   **kwargs)


class ContactFormRedirect(ContactForm):
    def __call__(self, *args, **kwargs):
        impressum = api.content.find(Title=IMPRESSUM)

        if impressum:
            self.request.response.redirect(
                impressum[0].getObject().absolute_url(),
            )
            return
        else:
            return super(ContactFormRedirect, self).__call__(*args, **kwargs)
