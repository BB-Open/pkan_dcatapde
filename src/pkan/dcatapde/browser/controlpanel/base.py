# -*- coding: utf-8 -*-
"""Base controlpanel view."""

from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from z3c.form import field
from zope.component import getUtility

from pkan.dcatapde import i18n


class SelfHealingRegistryEditForm(controlpanel.RegistryEditForm):
    """Registers the schema if an error occured."""

    def getContent(self):
        registry = getUtility(IRegistry)
        try:
            return registry.forInterface(  # noqa
                self.schema,
                prefix=self.schema_prefix,
            )
        except KeyError:
            self.ignoreContext = True
            self.fields = field.Fields()
            registry.registerInterface(self.schema)
            self.status = i18n.STATUS_REGISTRY_UPDATED
            return None
