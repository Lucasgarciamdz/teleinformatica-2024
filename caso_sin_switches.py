#!/usr/bin/env python
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import Host
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def myNetwork():
    net = Mininet(topo=None, build=False, ipBase='192.168.100.0/24')
    
    info('*** Add routers\n')

    # Adding routers with their WAN interface IP addresses
    r0 = net.addHost('r0', cls=Node, ip='192.168.100.6/29') # Casa matriz
    r1 = net.addHost('r1', cls=Node, ip='192.168.100.1/29')
    r2 = net.addHost('r2', cls=Node, ip='192.168.100.9/29')

    # Enabling IP forwarding on routers
    for router in [r0, r1, r2]:
        router.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Add hosts\n')
    h11 = net.addHost('h11', cls=Host, ip='10.0.1.1/24', defaultRoute="via 192.168.100.9/29")
    h21 = net.addHost('h21', cls=Host, ip='10.0.2.1/24', defaultRoute="via 192.168.100.17/29")

    info('*** Add links\n')
    # Adding links between routers
    net.addLink(r0, r1, intfName1='r0-eth11', intfName2='r1-eth11', params1={'ip': '192.168.100.6/29'}, params2={'ip': '192.168.100.1/29'})
    net.addLink(r0, r2, intfName1='r0-eth21', intfName2='r2-eth21', params1={'ip': '192.168.100.14/29'}, params2={'ip': '192.168.100.9/29'})
    
    # Adding links between routers and hosts
    net.addLink(r1, h11, intfName1='r1-eth21', intfName2='h11-eth0', params1={'ip': '10.0.1.1/24'}, params2={'ip': '10.0.1.254/24'})
    net.addLink(r2, h21, intfName1='r2-eth11', intfName2='h21-eth0', params1={'ip': '10.0.2.1/24'}, params2={'ip': '10.0.2.254/24'})

    info('*** Starting network\n')
    net.build()

    info('*** Post configure switches and hosts\n')
    
    # Setting up routing tables
    info('*** Creating routes\n')
    
    r0.cmd('ip route add 10.0.1.0/24 via 192.168.100.1/29 dev r0-eth11')
    r0.cmd('ip route add 10.0.2.0/24 via 192.168.100.9/29 dev r0-eth21')
    
    r1.cmd('ip route add 10.0.2.0/24 via 192.168.100.6/29 dev r1-eth11')
    r1.cmd('ip route add 192.168.100.8/29 via 192.168.100.6/29 dev r1-eth11')
    
    h11.cmd('ip route add 192.168.100.0/29 via 10.0.1.1/24 dev h11-eth0')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()