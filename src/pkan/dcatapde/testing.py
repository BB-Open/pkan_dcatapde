# -*- coding: utf-8 -*-
"""Test Layer for pkan.dcatapde."""

import responses
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import Layer
from plone.testing import z2

from pkan.dcatapde.tests import utils


class APIMockLayer(Layer):
    """Load test fixtures using responses to mock API requests."""

    def testSetUp(self):
        responses.start()
        utils.setup_fixtures()

    def testTearDown(self):
        try:
            responses.stop()
        except RuntimeError:
            pass
        finally:
            responses.reset()


APIMOCK = APIMockLayer()


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
    bases=(FIXTURE,),
    name='pkan.dcatapde:Integration',
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(APIMOCK, FIXTURE, z2.ZSERVER_FIXTURE),
    name='pkan.dcatapde:Functional',
)


class FunctionalAPIMockLayer(APIMockLayer):
    """Functional Tests with API Mock Layer."""

    defaultBases = (
        FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE,
    )


ACCEPTANCE_TESTING = FunctionalAPIMockLayer(
    name='pkan.dcatapde:Acceptance',
)

ROBOT_TESTING = APIMockLayer(name='pkan.dcatapde:Robot')
