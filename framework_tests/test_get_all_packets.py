# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest

from testing import integration_test as integration_test
from testing.tcpdump.Packet import Packet

# Network used in this test
from networks import sample_network as network


class TestAllPackets(integration_test.IntegrationTestCase):

    def setUp(self):
        # TestConfiguration
        self.CONTROLLER_PATH = '../../controller/routing_switch.py'
        self.NETWORK = network.Network
        super(TestAllPackets, self).setUp()

    def test_received_packet(self):
        self.analyze_packets("h1", lambda: self.net.pingAll())
        packet = Packet()
        all_packets = self.get_all_packets(packet)
        self.assertTrue(len(all_packets) > 0, "all_packets returns packet.")

if __name__ == '__main__':
    unittest.main()