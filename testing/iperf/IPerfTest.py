# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.

from IPerfClient import IPerfClient

class IPerfTest:

    def __init__(self, net):
        self.net = net
        self.server = None
        self.outputs = []

    def start_test(self, server, clients, server_parameter = "", client_parameter = []):
        self.server = self.net.get(server)
        self.__init_client_threads__(clients, client_parameter)
        self.__start_server__(server_parameter)
        self.__start_clients__()
        self.__stop_server__()
        self.__collect_outputs__()

    def __init_client_threads__(self, clients, client_parameter):
        self.client_threads = []
        for i in range(0, len(clients)):
            if i < len(client_parameter):
                c_param = client_parameter[i]
            else:
                c_param = ""
            server_ip = self.server.IP()
            t = IPerfClient(self.net, clients[i], c_param, server_ip)
            self.client_threads.append(t)

    def __start_server__(self, server_parameter):
        self.server_cmd = "iperf -s " + server_parameter + " &"
        self.server.cmd(self.server_cmd)

    def __start_clients__(self):
        for t in self.client_threads:
            t.start()
        for t in self.client_threads:
            t.join()

    def __stop_server__(self):
        self.server.cmd("kill %" + self.server_cmd)

    def __collect_outputs__(self):
        for t in self.client_threads:
            self.outputs.append(t.value)

    def get_transfer(self, index):
        colmns = self.outputs[index].split("\n")[6].split(" ")
        number = float(colmns[7])
        unit = colmns[8].strip(' \t\n\r')
        return number, unit

    def get_bandwidth(self, index):
        colmns = self.outputs[index].split("\n")[6].split(" ")
        number = float(colmns[10])
        unit = colmns[11].strip(' \t\n\r')
        return number, unit
