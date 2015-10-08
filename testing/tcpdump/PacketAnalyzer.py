# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.

import dpkt
import time
import socket
from Packet import Packet

class PacketAnalyzer:

    def __init__(self, file_name):
        self._file = open(file_name)
        time.sleep(0.1)
        self.pcap = dpkt.pcap.Reader(self._file)
        time.sleep(0.5)

        self.packets = []
        for ts, buf in self.pcap:
            try:
                packet = Packet()
                packet.time_stamp = ts

                eth = dpkt.ethernet.Ethernet(buf)
                src_mac = eth.src.encode("hex")
                dst_mac = eth.dst.encode("hex")
                packet.eth_src = ':'.join([src_mac[i:i+2] for i in range(0, len(src_mac), 2)])
                packet.eth_dst = ':'.join([dst_mac[i:i+2] for i in range(0, len(dst_mac), 2)])

                ip = eth.data
                packet.ip_version = ip.v
                if ip.v == 6:
                    packet.ip_src = socket.inet_ntop(socket.AF_INET6, ip.src)
                    packet.ip_dst = socket.inet_ntop(socket.AF_INET6, ip.dst)
                if ip.v == 4:
                    packet.ip_src = socket.inet_ntoa(ip.src)
                    packet.ip_dst = socket.inet_ntoa(ip.dst)

                if ip.p is dpkt.ip.IP_PROTO_TCP or ip.nxt is dpkt.ip.IP_PROTO_TCP:
                        tcp = ip.data
                        packet.tcp_src_port = tcp.sport
                        packet.tcp_dst_port = tcp.dport

                if ip.udp is not None:
                    packet.udp_src_port = ip.udp.sport
                    packet.udp_dst_port = ip.udp.dport


            except AttributeError:
                pass

            self.packets.append(packet)

    def is_packet_received(self, packet):
        attributes = filter(lambda a: not a.startswith('__'), dir(packet))
        for pkt in self.packets:
            match = True
            for attribute in attributes:
                if getattr(packet, attribute) is not None:
                    match = getattr(packet, attribute) == getattr(pkt, attribute)
            if match:
                return True

        return False

    def get_all_packets(self, packet):
        matches = []
        def_attr = False

        attributes = filter(lambda a: not a.startswith('__'), dir(packet))
        for pkt in self.packets:
            for attribute in attributes:
                if getattr(packet, attribute) is not None:
                    def_attr = True
                    if getattr(packet, attribute) == getattr(pkt, attribute):
                        matches.append(pkt)

        if not def_attr:
            matches = self.packets

        return matches

    def get_number_of_packet(self):
        return sum(1 for e in self.pcap)

    def close(self):
        self._file.close()
