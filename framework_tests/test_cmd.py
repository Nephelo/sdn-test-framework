# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
import logging

from testing import integration_test as integration_test

# Network used in this test
from networks import sample_network as network


class TestCmd(integration_test.IntegrationTestCase):

    def setUp(self):
        # TestConfiguration
        self.CONTROLLER_PATH = '../../controller/routing_switch.py'
        self.NETWORK = network.Network
        super(TestCmd, self).setUp()

    def test_execCmd(self):
        res = self.execCmd("h1", "echo 'Test'")
        self.assertEqual(res, "Test", "Executing command on host is working.")

if __name__ == '__main__':
    unittest.main()