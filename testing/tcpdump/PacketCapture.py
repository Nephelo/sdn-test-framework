# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.

import logging
import os
import time

class PacketCapture:

    def __init__(self, net):
        self.net = net

    def start_capture(self, host_name):
        self.host_name = host_name
        self.host = self.net.get(self.host_name)
        interface = self.host.intfs[0].name
        self.file_name = "/tmp/" + interface + ".pcap"

        if os.path.isfile(self.file_name):
            os.remove(self.file_name)

        self.command = "tcpdump"
        args = "-s 0 -i " + interface + " -w " + self.file_name + " &"

        logging.debug("running command: '" + self.command + " " + args + "' on host " + self.host_name)
        self.host.cmd(self.command, args)
        time.sleep(0.5)

    def stop_capture(self):
        time.sleep(0.75)
        logging.debug("stopping command: " + self.command + " on host " + self.host_name)
        self.host.cmd("kill %" + self.command)

    def get_file_name(self):
        return self.file_name
