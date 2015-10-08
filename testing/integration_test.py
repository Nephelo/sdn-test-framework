# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.

import unittest
import logging
logging.basicConfig(level=logging.DEBUG)
import time
import multiprocessing
from ryu.cmd.manager import main as ruy_main

from tcpdump.PacketCapture import PacketCapture
from tcpdump.PacketAnalyzer import PacketAnalyzer

class IntegrationTestCase(unittest.TestCase):

    def setUp(self):
        args = ['--ofp-tcp-listen-port', '16001']
        if isinstance(self.CONTROLLER_PATH, list):
            args.extend(self.CONTROLLER_PATH)
        else:
            args.append(self.CONTROLLER_PATH)
        self.p = multiprocessing.Process(target=ruy_main, args=(args,))
        self.p.start()
        self.net = self.NETWORK()

        self.analyzers = {}
        self.hosts = []

    def tearDown(self):
        logging.debug("Stopping Mininet and ryu")
        self.net.stop()
        self.p.terminate()

        if self._analyzer_available():
            self.analyzer.close()

    def assertAllReachable(self, message):
        packet_loss_rate = self.net.pingAll()
        self.assertEqual(packet_loss_rate, 0, message)

    def assertReachable(self, h1, h2, message):
        host1, host2 = self.net.get(h1, h2)
        packet_loss_rate = self.net.ping((host1, host2))
        self.assertEqual(packet_loss_rate, 0, message)

    def assertPacketIn(self, message, host=None):
        self.assertTrue(self._analyzer_available(), "Analyzer-Object is available")
        if host is None:
            host = self.hosts[0]
        self.assertTrue(self.analyzers[host].get_number_of_packet() > 0, message)

    def assertReceivedPacket(self, packet, message, host=None):
        self.assertTrue(self._analyzer_available(), "Analyzer-Object is available")
        if host is None:
            host = self.hosts[0]
        self.assertTrue(self.analyzers[host].is_packet_received(packet), message)

    def assertNotReceivedPacket(self, packet, message, host=None):
        self.assertTrue(self._analyzer_available(), "Analyzer-Object is available")
        if host is None:
            host = self.hosts[0]
        self.assertFalse(self.analyzers[host].is_packet_received(packet), message)

    def get_all_packets(self, packet, host=None):
        if host is None:
            host = self.hosts[0]
        return self.analyzers[host].get_all_packets(packet)

    def execCmd(self, h, cmd):
        logging.debug("Running command: " + cmd + " on host " + h)
        host = self.net.get(h)
        result = host.cmd(cmd)
        return result.strip(' \t\n\r')

    def send_ip4_packet(self, host, dst, ip_proto, content):
        cmd = "import socket \ns = socket.socket(socket.AF_INET, socket.SOCK_RAW, " + str(ip_proto) \
              + ") \ns.connect((\"" + dst + "\", 1)) \ns.send(\"" + content + "\")"
        self.execCmd(host, "python -c '" + cmd + "'")

    def analyze_packets(self, hosts, fun):
        captures = {}

        if not isinstance(hosts, list):
            hosts = [hosts]

        self.hosts = hosts

        # Start capture on each host
        for host in hosts:
            capture = PacketCapture(self.net)
            capture.start_capture(host)
            captures[host] = capture
        time.sleep(5)

        # Run the code to analyze
        fun()

        time.sleep(5)
        # Stop capture on all hosts
        for host in hosts:
            captures[host].stop_capture()
            self.analyzers[host] = PacketAnalyzer(captures[host].get_file_name())

        # Set default analyzer
        self.analyzer = self.analyzers[hosts[0]]

    def _analyzer_available(self):
        for host in self.hosts:
            try:
                self.analyzers[host]
                return True
            except AttributeError:
                return False

if __name__ == '__main__':
    unittest.main()
