# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
from testing.iperf.IPerfTest import IPerfTest

from testing import integration_test as integration_test

# Network used in this test
from networks import sample_network as network


class TestIPerf(integration_test.IntegrationTestCase):

    def setUp(self):
        # TestConfiguration
        self.CONTROLLER_PATH = '../../controller/routing_switch.py'
        self.NETWORK = network.Network
        super(TestIPerf, self).setUp()

    def test_iperf_on_one_host(self):
        iperf_test = IPerfTest(self.net)
        iperf_test.start_test("h1", ["h2"])
        transfer_number, transfer_unit = iperf_test.get_transfer(0)
        print("transfer: " + str(transfer_number) + " " + transfer_unit)
        bandwidth_number, bandwidth_unit = iperf_test.get_bandwidth(0)
        print("bandwidth: " + str(bandwidth_number) + " " + bandwidth_unit)

        self.assertEqual(transfer_unit, "GBytes", "Correct unit of iperf transfer.")
        self.assertEqual(bandwidth_unit, "Gbits/sec", "Correct unit of iperf bandwidth.")

        self.assertTrue(isinstance(transfer_number, float), "Transfer value is a number.")
        self.assertTrue(isinstance(bandwidth_number, float), "Bandwidth value is a number.")

    def test_iperf_on_multiple_hosts(self):
        iperf_test = IPerfTest(self.net)
        iperf_test.start_test("h1", ["h2", "h3"])

        transfer_number, transfer_unit = iperf_test.get_transfer(0)
        bandwidth_number, bandwidth_unit = iperf_test.get_bandwidth(0)
        transfer_number1, transfer_unit1 = iperf_test.get_transfer(1)
        bandwidth_number1, bandwidth_unit1 = iperf_test.get_bandwidth(1)

        self.assertEqual(transfer_unit, transfer_unit1,"Same unit for both hosts.")
        self.assertEqual(bandwidth_unit, bandwidth_unit1, "Same unit for both hosts.")

        self.assertTrue(abs(transfer_number - transfer_number1) < 5, "Transfered nearly same traffic on both hosts.")
        self.assertTrue(abs(bandwidth_number - bandwidth_number1) < 5, "Bandwidth nearly the same on both hosts.")

if __name__ == '__main__':
    unittest.main()