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
    s1 = net.addSwitch("s1", cls=OVSKernelSwitch, failMode="standalone")
    s2 = net.addSwitch("s2", cls=OVSKernelSwitch, failMode="standalone")
    s3 = net.addSwitch("s3", cls=OVSKernelSwitch, failMode="standalone")
    s4 = net.addSwitch("s4", cls=OVSKernelSwitch, failMode="standalone")
    s5 = net.addSwitch("s5", cls=OVSKernelSwitch, failMode="standalone")
    s6 = net.addSwitch("s6", cls=OVSKernelSwitch, failMode="standalone")

    s11 = net.addSwitch("s11", cls=OVSKernelSwitch, failMode="standalone")
    s22 = net.addSwitch("s22", cls=OVSKernelSwitch, failMode="standalone")
    s33 = net.addSwitch("s33", cls=OVSKernelSwitch, failMode="standalone")
    s44 = net.addSwitch("s44", cls=OVSKernelSwitch, failMode="standalone")
    s55 = net.addSwitch("s55", cls=OVSKernelSwitch, failMode="standalone")
    s66 = net.addSwitch("s66", cls=OVSKernelSwitch, failMode="standalone")



    info("*** Add routers\n")

    r0 = net.addHost('r0', cls=Node, ip='192.168.100.6')
    r0.cmd('sysctl -w net.ipv4.ip_forward=1')
    

    r1 = net.addHost('r1', cls=Node, ip='192.168.100.1')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    r2 = net.addHost('r2', cls=Node, ip='192.168.100.9')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')

    r3 = net.addHost('r3', cls=Node, ip='192.168.100.17')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    r4 = net.addHost('r4', cls=Node, ip='192.168.100.25')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')

    r5 = net.addHost('r5', cls=Node, ip='192.168.100.33')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')

    r6 = net.addHost('r6', cls=Node, ip='192.168.100.41')
    r6.cmd('sysctl -w net.ipv4.ip_forward=1')

    info("*** Add hosts\n")
    h1 = net.addHost("h1", cls=Host, ip="10.0.1.254/24")
    h2 = net.addHost("h2", cls=Host, ip="10.0.2.254/24")
    h3 = net.addHost("h3", cls=Host, ip="10.0.3.254/24")
    h4 = net.addHost("h4", cls=Host, ip="10.0.4.254/24")
    h5 = net.addHost("h5", cls=Host, ip="10.0.5.254/24")
    h6 = net.addHost("h6", cls=Host, ip="10.0.6.254/24")
    

    info("*** Add links\n")
    # Adding links between routers and switches
    net.addLink(r0, s1, intfName1="r0-eth1", params1={"ip": "192.168.100.6/29"})
    net.addLink(r0, s2, intfName1="r0-eth2", params1={"ip": "192.168.100.14/29"})
    net.addLink(r0, s3, intfName1="r0-eth3", params1={"ip": "192.168.100.22/29"})
    net.addLink(r0, s4, intfName1="r0-eth4", params1={"ip": "192.168.100.30/29"})
    net.addLink(r0, s5, intfName1="r0-eth5", params1={"ip": "192.168.100.38/29"})
    net.addLink(r0, s6, intfName1="r0-eth6", params1={"ip": "192.168.100.46/29"})

    # Adding links between switches and routers
    net.addLink(r1, s1, intfName1="r1-eth1", params1={"ip": "192.168.100.1/29"})
    net.addLink(r2, s2, intfName1="r1-eth2", params1={"ip": "192.168.100.9/29"})
    net.addLink(r3, s3, intfName1="r1-eth3", params1={"ip": "192.168.100.17/29"})
    net.addLink(r4, s4, intfName1="r1-eth4", params1={"ip": "192.168.100.25/29"})
    net.addLink(r5, s5, intfName1="r1-eth5", params1={"ip": "192.168.100.33/29"})
    net.addLink(r6, s6, intfName1="r1-eth6", params1={"ip": "192.168.100.41/29"})

    # Adding links between router and switch
    net.addLink(r1, s11, intfName1="r2-eth1", params1={"ip": "10.0.1.1/24"})
    net.addLink(r2, s22, intfName1="r2-eth2", params1={"ip": "10.0.2.1/24"})
    net.addLink(r3, s33, intfName1="r2-eth3", params1={"ip": "10.0.3.1/24"})
    net.addLink(r4, s44, intfName1="r2-eth4", params1={"ip": "10.0.4.1/24"})
    net.addLink(r5, s55, intfName1="r2-eth5", params1={"ip": "10.0.5.1/24"})
    net.addLink(r6, s66, intfName1="r2-eth6", params1={"ip": "10.0.6.1/24"})

    # Adding links between switches and hosts
    net.addLink(h1, s11, intfName1="h1-eth0", params1={"ip": "10.0.1.254/24"})
    net.addLink(h2, s22, intfName1="h2-eth0", params1={"ip": "10.0.2.254/24"})
    net.addLink(h3, s33, intfName1="h3-eth0", params1={"ip": "10.0.3.254/24"})
    net.addLink(h4, s44, intfName1="h4-eth0", params1={"ip": "10.0.4.254/24"})
    net.addLink(h5, s55, intfName1="h5-eth0", params1={"ip": "10.0.5.254/24"})
    net.addLink(h6, s66, intfName1="h6-eth0", params1={"ip": "10.0.6.254/24"})


    info("*** Starting network\n")
    net.build()

    for controller in net.controllers:
        controller.start()

    info("* Starting switches\n")
    net.get("s1").start([])
    net.get("s2").start([])
    net.get("s3").start([])
    net.get("s4").start([])
    net.get("s5").start([])
    net.get("s6").start([])
    net.get("s11").start([])
    net.get("s22").start([])
    net.get("s33").start([])
    net.get("s44").start([])
    net.get("s55").start([])
    net.get("s66").start([])

    info("*** Post configure switches and hosts\n")

    # Setting up routing tables
    info("*** Creating routes\n")

    #crep qie es /21
    r0.cmd("ip route add 10.0.1.0/24 via 192.168.100.1 dev r0-eth1")
    r0.cmd("ip route add 10.0.2.0/24 via 192.168.100.9 dev r0-eth2")
    r0.cmd("ip route add 10.0.3.0/24 via 192.168.100.17 dev r0-eth3")
    r0.cmd("ip route add 10.0.4.0/24 via 192.168.100.25 dev r0-eth4")
    r0.cmd("ip route add 10.0.5.0/24 via 192.168.100.33 dev r0-eth5")
    r0.cmd("ip route add 10.0.6.0/24 via 192.168.100.41 dev r0-eth6")

    r1.cmd("ip route add 10.0.0.0/21 via 192.168.100.6 dev r1-eth1")
    r2.cmd("ip route add 10.0.0.0/21 via 192.168.100.14 dev r1-eth2")
    r3.cmd("ip route add 10.0.0.0/21 via 192.168.100.22 dev r1-eth3")
    r4.cmd("ip route add 10.0.0.0/21 via 192.168.100.30 dev r1-eth4")
    r5.cmd("ip route add 10.0.0.0/21 via 192.168.100.38 dev r1-eth5")
    r6.cmd("ip route add 10.0.0.0/21 via 192.168.100.46 dev r1-eth6")

    r1.cmd("ip route add 192.168.100.0/26 via 192.168.100.6 dev r1-eth1")
    r2.cmd("ip route add 192.168.100.0/26 via 192.168.100.14 dev r1-eth2")
    r3.cmd("ip route add 192.168.100.0/26 via 192.168.100.22 dev r1-eth3")
    r4.cmd("ip route add 192.168.100.0/26 via 192.168.100.30 dev r1-eth4")
    r5.cmd("ip route add 192.168.100.0/26 via 192.168.100.38 dev r1-eth5")
    r6.cmd("ip route add 192.168.100.0/26 via 192.168.100.46 dev r1-eth6")

    h1.cmd("ip route add 10.0.0.0/21 via 10.0.1.1 dev h1-eth0")
    h2.cmd("ip route add 10.0.0.0/21 via 10.0.2.1 dev h2-eth0")
    h3.cmd("ip route add 10.0.0.0/21 via 10.0.3.1 dev h3-eth0")
    h4.cmd("ip route add 10.0.0.0/21 via 10.0.4.1 dev h4-eth0")
    h5.cmd("ip route add 10.0.0.0/21 via 10.0.5.1 dev h5-eth0")
    h6.cmd("ip route add 10.0.0.0/21 via 10.0.6.1 dev h6-eth0")

    h1.cmd("ip route add 192.168.100.0/26 via 10.0.1.1 dev h1-eth0")
    h2.cmd("ip route add 192.168.100.0/26 via 10.0.2.1 dev h2-eth0")
    h3.cmd("ip route add 192.168.100.0/26 via 10.0.3.1 dev h3-eth0")
    h4.cmd("ip route add 192.168.100.0/26 via 10.0.4.1 dev h4-eth0")
    h5.cmd("ip route add 192.168.100.0/26 via 10.0.5.1 dev h5-eth0")
    h6.cmd("ip route add 192.168.100.0/26 via 10.0.6.1 dev h6-eth0")

    


    

    


    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    myNetwork()
