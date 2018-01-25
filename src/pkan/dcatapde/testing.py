# -*- coding: utf-8 -*-
"""Test Layer for pkan.dcatapde."""

from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import Layer
from plone.testing import z2


class Fixture(PloneSandboxLayer):
    """Custom Test Layer for pkan.dcatapde."""

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope for testing."""
        # Load ZCML
        import pkan.dcatapde
        self.loadZCML(package=pkan.dcatapde)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'pkan.dcatapde:default')


FIXTURE = Fixture()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE, ),
    name='pkan.dcatapde:Integration',
)


FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, z2.ZSERVER_FIXTURE),
    name='pkan.dcatapde:Functional',
)


ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name='pkan.dcatapde:Acceptance',
)


ROBOT_TESTING = Layer(name='pkan.dcatapde:Robot')
