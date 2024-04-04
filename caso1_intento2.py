#!/usr/bin/env python
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import OVSKernelSwitch
from mininet.node import Host
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def myNetwork():
    net = Mininet(topo=None, build=False, ipBase="192.168.100.0/24")

    info("*** Add switches\n")
    s11 = net.addSwitch("s11", cls=OVSKernelSwitch, failMode="standalone")
    s12 = net.addSwitch("s12", cls=OVSKernelSwitch, failMode="standalone")
    s21 = net.addSwitch("s21", cls=OVSKernelSwitch, failMode="standalone")
    s22 = net.addSwitch("s22", cls=OVSKernelSwitch, failMode="standalone")

    info("*** Add routers\n")

    r0 = net.addHost('r0', cls=Node, ip='192.168.100.6')
    r0.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    #ROUTERS HIJOS
    r1 = net.addHost('r1', cls=Node, ip='192.168.100.1')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    r2 = net.addHost('r2', cls=Node, ip='192.168.100.9')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')

    info("*** Add hosts\n")
    h11 = net.addHost("h11", cls=Host, ip="10.0.1.254/24")
    h21 = net.addHost("h21", cls=Host, ip="10.0.2.254/24")

    info("*** Add links\n")
    # Adding links between routers and switches
    net.addLink(r0, s11, intfName1="r0-eth11", params1={"ip": "192.168.100.6/29"})
    net.addLink(r0, s21, intfName1="r0-eth21", params1={"ip": "192.168.100.14/29"})

    # Adding links between switches and routers
    net.addLink(r1, s11, intfName1="r1-eth11", params1={"ip": "192.168.100.1/29"})
    net.addLink(r2, s21, intfName1="r2-eth21", params1={"ip": "192.168.100.9/29"})

    # Adding links between router and switch
    net.addLink(r1, s12, intfName1="r1-eth12", params1={"ip": "10.0.1.1/24"})
    net.addLink(r2, s22, intfName1="r2-eth22", params1={"ip": "10.0.2.1/24"})

    # Adding links between switches and hosts
    net.addLink(h11, s12, intfName1="h11-eth0", params1={"ip": "10.0.1.254/24"})
    net.addLink(h21, s22, intfName1="h21-eth0", params1={"ip": "10.0.2.254/24"})

    info("*** Starting network\n")
    net.build()

    for controller in net.controllers:
        controller.start()

    info("* Starting switches\n")
    net.get("s11").start([])
    net.get("s21").start([])
    net.get("s12").start([])
    net.get("s22").start([])

    info("*** Post configure switches and hosts\n")

    # Setting up routing tables
    info("*** Creating routes\n")

    r0.cmd("ip route add 10.0.1.0/24 via 192.168.100.1 dev r0-eth11")
    r0.cmd("ip route add 10.0.2.0/24 via 192.168.100.9 dev r0-eth21")

    r1.cmd("ip route add 10.0.2.0/24 via 192.168.100.6 dev r1-eth11")
    r1.cmd("ip route add 192.168.100.8/29 via 192.168.100.6 dev r1-eth11")

    r2.cmd("ip route add 10.0.1.0/24 via 192.168.100.14 dev r2-eth21")
    r2.cmd("ip route add 192.168.100.0/29 via 192.168.100.14 dev r2-eth21")

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
