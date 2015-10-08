# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.

from threading import Thread


class IPerfClient(Thread):

    def __init__(self, net, client, args, server):
        self.net = net
        self.server = server
        self.args = args
        self.client = net.get(client)
        self.value = ""
        super(IPerfClient, self).__init__()

    def run(self):
        cmd = "iperf -c " + self.server + " " + self.args
        self.value = self.client.cmd(cmd)

