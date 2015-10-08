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


class TestPacketAnalyzer(integration_test.IntegrationTestCase):

    def setUp(self):
        # TestConfiguration
        self.CONTROLLER_PATH = '../../controller/routing_switch.py'
        self.NETWORK = network.Network
        super(TestPacketAnalyzer, self).setUp()

    def test_received_packets(self):
        self.analyze_packets(["h1","h2"], lambda: self.net.pingAll())
        self.assertPacketIn("Host 1 received a packet", "h1")

    def test_received_eth_packet(self):
        host1, host2 = self.net.get("h1", "h2")
        self.analyze_packets(["h1","h2"], lambda: self.net.ping((host1, host2)))

        # Analyze packets on h1
        packet = Packet()
        packet.eth_src = "cc:cc:cc:cc:cc:01"
        packet.eth_dst = "cc:cc:cc:cc:cc:02"
        self.assertReceivedPacket(packet, "Received eth packet", "h1")
        packet1 = Packet()
        packet1.eth_src = "aa:aa:aa:aa:aa:aa"
        packet1.eth_dst = "cc:cc:cc:cc:cc:02"
        self.assertNotReceivedPacket(packet1, "Not received packet from switch.", "h1")

        # Analyze packets on h2
        packet3 = Packet()
        packet3.eth_src = "cc:cc:cc:cc:cc:01"
        packet3.eth_dst = "cc:cc:cc:cc:cc:02"
        self.assertReceivedPacket(packet3, "Received eth packet", "h2")
        packet4 = Packet()
        packet4.eth_src = "aa:aa:aa:aa:aa:aa"
        packet4.eth_dst = "cc:cc:cc:cc:cc:02"
        self.assertNotReceivedPacket(packet4, "Not received packet from switch.", "h2")

if __name__ == '__main__':
    unittest.main()