# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
import dpkt
import random

from testing import integration_test as integration_test
from testing.tcpdump.Packet import Packet

# Network used in this test
from networks import sample_network as network


class TestSendPacket(integration_test.IntegrationTestCase):

    def setUp(self):
        # TestConfiguration
        self.CONTROLLER_PATH = '../../controller/routing_switch.py'
        self.NETWORK = network.Network
        super(TestSendPacket, self).setUp()

    def test_send_icmp(self):

        icmp_cont = dpkt.icmp.ICMP.Echo()
        icmp_cont.data = 'icmp echo'
        icmp_cont.seq = random.randint(0, 65535)
        icmp_cont.id = random.randint(0, 65535)

        icmp_packet = dpkt.icmp.ICMP()
        icmp_packet.type = dpkt.icmp.ICMP_ECHO
        icmp_packet.data = icmp_cont

        self.analyze_packets("h2", lambda: self.send_ip4_packet("h1", "192.168.0.2", dpkt.ip.IP_PROTO_ICMP, str(icmp_packet)))
        packet = Packet()
        packet.ip_src = "192.168.0.1"
        packet.ip_dst = "192.168.0.2"
        self.assertReceivedPacket(packet, "Received sent icmp packet", "h2")

if __name__ == '__main__':
    unittest.main()