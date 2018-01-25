# -*- coding: utf-8 -*-
"""Test UI with robot framework."""

from pkan.dcatapde import testing
from plone import api
from plone.testing import layered

import os
import robotsuite
import unittest


def test_suite():
    """Create the robot test suite."""
    suite = unittest.TestSuite()
    no_robot = 'NO_ROBOT' in os.environ.keys()
    if no_robot or api.env.plone_version() < '4.2':
        # No robot tests for Plone 4.1.x
        return suite

    current_dir = os.path.abspath(os.path.dirname(__file__))
    robot_dir = os.path.join(current_dir, 'robot')
    robot_tests = [
        os.path.join('robot', doc)
        for doc in os.listdir(robot_dir)
        if doc.endswith('.robot') and doc.startswith('test_')
    ]
    for robot_test in robot_tests:
        suite.addTests([
            layered(
                robotsuite.RobotTestSuite(robot_test),
                layer=testing.ROBOT_TESTING,
            ),
        ])
    return suite
