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

    def test_timestamps(self):
        self.analyze_packets(["h1","h3"], lambda: self.net.pingAll())
        packet_1_to_2 = Packet()
        packet_1_to_2.ip_src = "192.168.0.1"
        packet_1_to_2.ip_dst = "192.168.0.2"

        packet_3_to_4 = Packet()
        packet_3_to_4.ip_src = "192.168.0.3"
        packet_3_to_4.ip_dst = "192.168.0.4"
        time_1_to_2 = self.get_all_packets(packet_1_to_2, "h1")[0].time_stamp
        time_3_to_4 = self.get_all_packets(packet_3_to_4, "h3")[0].time_stamp
        self.assertTrue(time_3_to_4 > time_1_to_2, "Timestamp ordering ok. Ping from h1 to h2 is sent first.")

if __name__ == '__main__':
    unittest.main()