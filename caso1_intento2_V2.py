#!/usr/bin/env python
from mininet.net import Mininet
from mininet.node import Node, OVSKernelSwitch, Host
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def myNetwork():
    net = Mininet(topo=None, build=False, ipBase="192.168.100.0/24")

    info("*** Add switches\n")
    switches = [net.addSwitch(f"s{i}", cls=OVSKernelSwitch, failMode="standalone") for i in range(1, 7)]
    switches += [net.addSwitch(f"s{i}{i}", cls=OVSKernelSwitch, failMode="standalone") for i in range(1, 7)]

    info("*** Add routers\n")
    routers = [net.addHost(f"r{i}", cls=Node, ip=f"192.168.100.{1+((i-1)*8)}") for i in range(1,7)]
    routers= [net.addHost('r0', cls=Node, ip=f"192.168.100.6")] + routers
    for router in routers:
        router.cmd('sysctl -w net.ipv4.ip_forward=1')

    info("*** Add hosts\n")
    hosts = [net.addHost(f"h{i}", cls=Host, ip=f"10.0.{i}.254/24") for i in range(1, 7)]

    info("*** Add links\n")
    for i in range(6):
        net.addLink(routers[0], switches[i], intfName1=f"r0-eth{i+1}", params1={"ip": f"192.168.100.{i*8+6}/29"})
        net.addLink(routers[i+1], switches[i], intfName1=f"r1-eth{i+1}", params1={"ip": f"192.168.100.{i*8+1}/29"})
        net.addLink(routers[i+1], switches[i+6], intfName1=f"r2-eth{i+1}", params1={"ip": f"10.0.{i+1}.1/24"})
        net.addLink(hosts[i], switches[i+6], intfName1=f"h{i+1}-eth0", params1={"ip": f"10.0.{i+1}.254/24"})

    info("*** Starting network\n")
    net.build()

    for controller in net.controllers:
        controller.start()

    info("* Starting switches\n")
    for switch in switches:
        switch.start([])

    info("*** Post configure switches and hosts\n")

    # Setting up routing tables
    info("*** Creating routes\n")
    for i in range(6):
        routers[0].cmd(f"ip route add 10.0.{i+1}.0/24 via 192.168.100.{i*8+1} dev r0-eth{i+1}")
        routers[i+1].cmd(f"ip route add 10.0.0.0/21 via 192.168.100.{6+i*8} dev r1-eth{i+1}")
        routers[i+1].cmd(f"ip route add 192.168.100.0/26 via 192.168.100.{6+i*8} dev r1-eth{i+1}")
        hosts[i].cmd(f"ip route add 10.0.0.0/21 via 10.0.{i+1}.1 dev h{i+1}-eth0")
        hosts[i].cmd(f"ip route add 192.168.100.0/26 via 10.0.{i+1}.1 dev h{i+1}-eth0")

    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    myNetwork()