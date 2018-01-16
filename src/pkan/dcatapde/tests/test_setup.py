# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from pkan.dcatapde.testing import PKAN_DCATAPDE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that pkan.dcatapde is properly installed."""

    layer = PKAN_DCATAPDE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if pkan.dcatapde is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'pkan.dcatapde'))

    def test_browserlayer(self):
        """Test that IPkanDcatapdeLayer is registered."""
        from pkan.dcatapde.interfaces import (
            IPkanDcatapdeLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IPkanDcatapdeLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PKAN_DCATAPDE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['pkan.dcatapde'])

    def test_product_uninstalled(self):
        """Test if pkan.dcatapde is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'pkan.dcatapde'))

    def test_browserlayer_removed(self):
        """Test that IPkanDcatapdeLayer is removed."""
        from pkan.dcatapde.interfaces import \
            IPkanDcatapdeLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           IPkanDcatapdeLayer,
           utils.registered_layers())
