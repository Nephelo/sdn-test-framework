# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
import os
from testing.tcpdump.PacketCapture import PacketCapture

from testing import integration_test as integration_test

# Network used in this test
from networks import sample_network as network


class TestPacketCapture(integration_test.IntegrationTestCase):

    def setUp(self):
        # TestConfiguration
        self.CONTROLLER_PATH = '../../controller/routing_switch.py'
        self.NETWORK = network.Network
        super(TestPacketCapture, self).setUp()

    def test_dump_right_file_name(self):
        capture = PacketCapture(self.net)
        capture.start_capture("h1")
        capture.stop_capture()
        self.assertEqual(capture.get_file_name(), "/tmp/h1-eth0.pcap", "TCP-Dump uses right file.")

    def test_dump_file_exists(self):
        capture = PacketCapture(self.net)
        capture.start_capture("h1")
        capture.stop_capture()
        self.assertTrue(os.path.isfile("/tmp/h1-eth0.pcap"), "pcap file exists")

    def test_dump_file_override(self):
        capture = PacketCapture(self.net)
        capture.start_capture("h1")
        capture.stop_capture()

        file_name = capture.get_file_name()
        first_create_time = os.path.getctime(file_name)

        capture = PacketCapture(self.net)
        capture.start_capture("h1")
        capture.stop_capture()

        second_create_time = os.path.getctime(file_name)
        self.assertTrue(second_create_time > first_create_time, "pcap is overriden on second run")

if __name__ == '__main__':
    unittest.main()