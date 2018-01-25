# -*- coding: utf-8 -*-
"""Setup tests for this package."""

from pkan.dcatapde.testing import PKAN_DCATAPDE_INTEGRATION_TESTING
from plone import api
from plone.browserlayer.utils import registered_layers

import unittest


class TestSetup(unittest.TestCase):
    """Validate setup process for pkan.dcatapde."""

    layer = PKAN_DCATAPDE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Validate that our product is installed."""
        self.assertTrue(
            self.installer.isProductInstalled('pkan.dcatapde'),
        )

    def test_browserlayer(self):
        """Validate that the browserlayer for our product is installed."""
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('IPkanDcatapdeLayer', layers)


class TestUninstall(unittest.TestCase):
    """Validate uninstall process for pkan.dcatapde."""

    layer = PKAN_DCATAPDE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['pkan.dcatapde'])

    def test_product_uninstalled(self):
        """Validate that our product is uninstalled."""
        self.assertFalse(
            self.installer.isProductInstalled('pkan.dcatapde'),
        )

    def test_browserlayer_removed(self):
        """Validate that the browserlayer is removed."""
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('IPkanDcatapdeLayer', layers)
