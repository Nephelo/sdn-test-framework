# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest

import testing.integration_test as integration_test

# Network used in this test
import networks.sample_network as network


class MultipleControllers(integration_test.IntegrationTestCase):

    def setUp(self):
        # TestConfiguration
        self.CONTROLLER_PATH = ['../../controller/routing_switch.py', '../../controller/controller.py']
        self.NETWORK = network.Network
        super(MultipleControllers, self).setUp()

    def test_pingAll(self):
        packetLossRate = self.net.pingAll()
        self.assertEqual(packetLossRate, 0, "Packet loss rate of ping all is 0.")


if __name__ == '__main__':
    unittest.main()