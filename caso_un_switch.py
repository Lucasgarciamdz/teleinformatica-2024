#!/usr/bin/env python
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import OVSKernelSwitch
from mininet.node import Host
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def myNetwork():
    net = Mininet(topo=None, build=False, ipBase="192.168.100.0/24")
# Add switches
    info("*** Add switches\n")
    s1 = net.addSwitch("s1", cls=OVSKernelSwitch, failMode="standalone")
    s2 = net.addSwitch("s2", cls=OVSKernelSwitch, failMode="standalone")
    
    info("*** Add routers\n")

    r0 = net.addHost('r0', cls=Node, ip='192.168.100.6')
    r0.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    r1 = net.addHost('r1', cls=Node, ip='192.168.100.1')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    r2 = net.addHost('r2', cls=Node, ip='192.168.100.9')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')


    info("*** Add hosts\n")
    h11 = net.addHost("h11", cls=Host, ip="10.0.1.254/24")
    h21 = net.addHost("h21", cls=Host, ip="10.0.2.254/24")

    info("*** Add links\n")
    # Adding links between routers
    net.addLink(r0, r1, intfName1="r0-eth1", intfName2="r1-eth1", params1={"ip": "192.168.100.6/29"}, params2={"ip": "192.168.100.1/29"})
    net.addLink(r0, r2, intfName1="r0-eth2", intfName2="r2-eth1", params1={"ip": "192.168.100.14/29"}, params2={"ip": "192.168.100.9/29"})

    # # Adding links between routers and hosts
    # net.addLink(r1, h11, intfName1="r1-eth0", params1={"ip": "10.0.1.254/24"})
    # net.addLink(r2, h21, intfName1="r2-eth0", params1={"ip": "10.0.2.254/24"})

    # Add links between routers and switches
    net.addLink(r1, s1, intfName1="r1-eth0", params1={"ip": "10.0.1.1/24"})
    net.addLink(r2, s2, intfName1="r2-eth0", params1={"ip": "10.0.2.1/24"})

    # Add links between switches and hosts
    net.addLink(s1, h11, intfName2="h11-eth0", params2={"ip": "10.0.1.254/24"})
    net.addLink(s2, h21, intfName2="h21-eth0", params2={"ip": "10.0.2.254/24"})


        
    info("*** Starting network\n")
    net.build()

    # for node in net.hosts:
    #     node.cmd('/etc/init.d/networking restart')

    for controller in net.controllers:
        controller.start()

    info("* Starting switches\n")
    net.get("s1").start([])
    net.get("s2").start([])

    info("*** Post configure switches and hosts\n")

    # Setting up routing tables
    info("*** Creating routes\n")

    r0.cmd("ip route add 10.0.1.0/24 via 192.168.100.1 dev r0-eth1")
    r0.cmd("ip route add 10.0.2.0/24 via 192.168.100.9 dev r0-eth2")

    r1.cmd("ip route add 10.0.2.0/24 via 192.168.100.6 dev r1-eth1")
    r1.cmd("ip route add 192.168.100.8/29 via 192.168.100.6 dev r1-eth1")

    r2.cmd("ip route add 10.0.1.0/24 via 192.168.100.14 dev r2-eth1")
    r2.cmd("ip route add 192.168.100.0/29 via 192.168.100.14 dev r2-eth1")

  
    # Correct these lines
    h11.cmd("ip route add 192.168.100.0/29 via 10.0.1.1 dev h11-eth0")
    h11.cmd("ip route add 192.168.100.8/29 via 10.0.1.1 dev h11-eth0")
    h11.cmd("ip route add 10.0.2.0/24 via 10.0.1.1 dev h11-eth0")

    h21.cmd("ip route add 10.0.1.0/24 via 10.0.2.1 dev h21-eth0")
    h21.cmd("ip route add 192.168.100.0/29 via 10.0.2.1 dev h21-eth0")
    h21.cmd("ip route add 192.168.100.8/29 via 10.0.2.1 dev h21-eth0")
    CLI(net)
    net.stop()  


if __name__ == "__main__":
    setLogLevel("info")
    myNetwork()
