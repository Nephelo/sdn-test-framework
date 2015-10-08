# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.


import logging
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch

def Network():

    logging.debug("Starting sample_network")

    net = Mininet(topo=None, build=False)

    # create the nodes
    h1 = net.addHost('h1', ip='192.168.0.1/24')
    h2 = net.addHost('h2', ip='192.168.0.2/24')
    h3 = net.addHost('h3', ip='192.168.0.3/24')
    h4 = net.addHost('h4', ip='192.168.0.4/24')
    
    # create the switch
    s1 = net.addSwitch('s1', OVSSwitch, listenPort=16001)

    # create the links
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)
    
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
