# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.


import logging
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch, CPULimitedHost


def Network():

    logging.debug("Starting sample_network")

    net = Mininet(topo=None, build=False, host=CPULimitedHost, link=TCLink)

    # create the nodes
    # nodes have a limited CPU power of 10% of the system CPU
    h1 = net.addHost('h1', ip='192.168.0.1/24', cpu=0.1)
    h2 = net.addHost('h2', ip='192.168.0.2/24', cpu=0.1)
    h3 = net.addHost('h3', ip='192.168.0.3/24', cpu=0.1)
    h4 = net.addHost('h4', ip='192.168.0.4/24', cpu=0.1)
    
    # create the switch
    s1 = net.addSwitch('s1', OVSSwitch, listenPort=16001)

    # create the links
    # Link with bandwidth of 2 Mbps
    net.addLink(h1, s1, bw=2)
    # Link with delay of 10 ms
    net.addLink(h2, s1, delay='10ms')
    # Link with packet loss rate of 15%
    net.addLink(h3, s1, loss=15)
    # Link with queue size of 200 packets
    net.addLink(h4, s1, max_queue_size=200)
    
    # add controller
    controller = net.addController('c', controller=RemoteController, ip="127.0.0.1", port=16001, protocols='OpenFlow13')
    net.build()

    # connect controller
    s1.start( [controller] )
    # set open flow version
    s1.cmd('ovs-vsctl set Bridge s1 protocols=OpenFlow13')
    
    # looks like the mac setter in the addHist function doesn't work, so we handle this here
    s1.setMAC("aa:aa:aa:aa:aa:aa")
    h1.setMAC("cc:cc:cc:cc:cc:01")
    h2.setMAC("cc:cc:cc:cc:cc:02")
    h3.setMAC("cc:cc:cc:cc:cc:03")
    h4.setMAC("cc:cc:cc:cc:cc:04")
     
    return net
