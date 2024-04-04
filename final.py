#!/usr/bin/python

from subprocess import call

from mininet.cli import CLI
from mininet.link import Intf, TCLink
from mininet.log import info, setLogLevel
from mininet.net import Mininet
from mininet.node import (
    Host,
    Node,
    OVSKernelSwitch,
    RemoteController,
    UserSwitch,
)


def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='192.168.100.0/24')

    info( '* Adding controller\n' )
    info( '* Add switches\n')
    
    #SWITCHES
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, failMode='standalone')

    #ROUTER PADRE
    r0 = net.addHost('r0', cls=Node, ip='192.168.100.6')
    r0.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    #ROUTERS HIJOS
    r1 = net.addHost('r1', cls=Node, ip='192.168.100.1')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    r2 = net.addHost('r2', cls=Node, ip='192.168.100.9')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    
    info( '* Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.254/24')#, defaultRoute='192.168.100.9/29')
    h2 = net.addHost('h2', cls=Host, ip='10.0.2.254/24')#, defaultRoute='192.168.100.17/29')

    info( '* Add links\n')
    net.addLink(r0, s1, intfName1='r0s1-eth0',params1={'ip':'192.168.100.6/29'})
    net.addLink(r0, s2, intfName1='r0s2-eth0',params1={'ip':'192.168.100.14/29'})
    #net.addLink(r0, s3)
    net.addLink(r1, s1,intfName1='r1s1-eth0',params1={'ip':'192.168.100.1/29'})
    net.addLink(r2, s2,intfName1='r2s2-eth0',params1={'ip':'192.168.100.9/29'})
    #net.addLink(r3, s3)
    net.addLink(r1, s3,intfName1='r1s3-eth0',params1={'ip':'10.0.1.1/24'})
    net.addLink(r2, s4,intfName1='r2s4-eth0',params1={'ip':'10.0.2.1/24'})
    #net.addLink(r3, s6)
    
    net.addLink(h1, s3, intfName1='h1s3-eth0',params1={'ip':'10.0.1.254/24'})
    net.addLink(h2, s4, intfName1='h2s4-eth0',params1={'ip':'10.0.2.254/24'})

    info( '* Starting network\n')
    net.build()

    info( '* Creating routes:\n')
    info('\n- from h1s')

    info( '* Starting controllers\n')
    #TABLA DE ROUTEO DE R0
    info('\n- from r0 to h1',r0.cmd('ip r add 10.0.1.0/24 via 192.168.100.1 dev r0s1-eth0'))
    info('\n- from r0 to h2',r0.cmd('ip r add 10.0.2.0/24 via 192.168.100.9 dev r0s2-eth0'))

    #TABLA DE ROUTEO DE R1
    info('\n- from r1 to r2',r1.cmd('ip r add 192.168.100.8/29 via 192.168.100.6 dev r1s1-eth0'))
    info('\n- from r1 to h2',r1.cmd('ip r add 10.0.2.0/24 via 192.168.100.6 dev r1s1-eth0'))

    #TABLA DE ROUTEO DE R2
    info('\n- from r2 to r1',r2.cmd('ip r add 192.168.100.0/29 via 192.168.100.14 dev r2s2-eth0'))
    info('\n- from r2 to h1',r2.cmd('ip r add 10.0.1.0/24 via 192.168.100.14 dev r2s2-eth0'))

    #TABLA DE HOST 1
    info('\n- from h1 to r1',h1.cmd('ip r add 192.168.100.0/29 via 10.0.1.1 dev h1s3-eth0'))
    info('\n- from h1 to r2',h1.cmd('ip r add 192.168.100.8/29 via 10.0.1.1 dev h1s3-eth0'))
    info('\n- from h1 to h2',h1.cmd('ip r add 10.0.2.0/24 via 10.0.1.1 dev h1s3-eth0'))

    #TABLA DE ROUTEO DE H2
    info('\n- from h2 to r2',h2.cmd('ip r add 192.168.100.8/29 via 10.0.2.1 dev h2s4-eth0'))
    info('\n- from h2 to r1',h2.cmd('ip r add 192.168.100.0/29 via 10.0.2.1 dev h2s4-eth0'))
    info('\n- from h2 to h1',h2.cmd('ip r add 10.0.1.0/24 via 10.0.2.1 dev h2s4-eth0'))

    for controller in net.controllers:
        controller.start()

    info( '* Starting switches\n')
    net.get('s1').start([])
    net.get('s2').start([])
    net.get('s3').start([])
    net.get('s4').start([])


    info( '* Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()