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

    def test_number_of_packets(self):
        self.analyze_packets("h1", lambda: self.net.pingAll())
        number = self.analyzer.get_number_of_packet()
        self.assertTrue(number > 0, "Read packets from capture")

    def test_received_packets(self):
        self.analyze_packets("h1", lambda: self.net.pingAll())
        self.assertPacketIn("Host 1 received a packet")

    def test_empty_ref_packet(self):
        self.analyze_packets("h1", lambda: self.net.pingAll())
        packet = Packet()
        self.assertReceivedPacket(packet, "Received packet. Used empty reference packet")

    def test_received_eth_packet(self):
        self.analyze_packets("h1", lambda: self.net.pingAll())
        packet = Packet()
        packet.eth_src = "cc:cc:cc:cc:cc:01"
        packet.eth_dst = "cc:cc:cc:cc:cc:02"
        self.assertReceivedPacket(packet, "Received eth packet")
        packet1 = Packet()
        packet1.eth_src = "aa:aa:aa:aa:aa:aa"
        packet1.eth_dst = "cc:cc:cc:cc:cc:02"
        self.assertNotReceivedPacket(packet1, "Not received packet from switch.")

    def test_received_ip_packet(self):
        self.analyze_packets("h1", lambda: self.net.pingAll())
        packet = Packet()
        packet.ip_src = "192.168.0.1"
        packet.ip_dst = "192.168.0.2"
        self.assertReceivedPacket(packet, "Received ip packet")
        packet1 = Packet()
        packet1.ip_src = "192.168.0.254"
        packet1.ip_dst = "192.168.0.2"
        self.assertNotReceivedPacket(packet1, "Not received packet from unknown ip.")

    def test_ip_v6(self):
        self.analyze_packets("h1", lambda: self.net.pingAll())
        packet = Packet()
        packet.ip_version = 6
        packet.ip_dst = "ff02::16"
        self.assertReceivedPacket(packet, "Received IPv6-Packet")


    def test_tcp(self):
        # start netcat server
        self.execCmd("h2", "nc -l 12345 &")
        pid = self.net.get("h2").lastPid

        # send packets
        self.analyze_packets("h1", lambda: self.execCmd("h1", "echo 'TEST' | nc 192.168.0.2 12345"))

        # stop netcat server
        self.execCmd("h2", "kill " + str(pid))

        # analyze packets
        packet = Packet()
        packet.ip_src = "192.168.0.1"
        packet.ip_dst = "192.168.0.2"
        packet.tcp_dst_port = 12345
        self.assertReceivedPacket(packet, "TCP Packet Received")

if __name__ == '__main__':
    unittest.main()