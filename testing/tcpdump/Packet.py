# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.

class Packet:
    def __init__(self):
        self.time_stamp = None
        self.eth_dst = None
        self.eth_src = None
        self.ip_src = None
        self.ip_dst = None
        self.ip_version = None
        self.tcp_src_port = None
        self.tcp_dst_port = None
        self.udp_src_port = None
        self.udp_dst_port = None
