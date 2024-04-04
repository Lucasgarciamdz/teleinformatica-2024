#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    
    puestos_de_trabajo = [net.addHost(f'Puesto de trabajo S{i}', cls=Host, ip=f'10.0.{i}.254', defaultRoute=None) for i in range(1, 3)]

    info( '*** Add links\n')
    net.addLink(r1, r2)
    net.addLink(r1, r3)
    net.addLink(r2, h1)
    net.addLink(r3, h2)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()


from mininet.net import Mininet
from mininet.node import Node, OVSKernelSwitch, RemoteController
from mininet.link import TCLink

# Crear la topología de la red
net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink)

# Agregar el controlador
controller = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

# Crear el router de la casa matriz
router_casa_matriz = net.addHost('router_casa_matriz')
router_casa_matriz.cmd('ifconfig router_casa_matriz-eth0 192.168.100.7 netmask 255.255.255.248')
router_casa_matriz.cmd('ifconfig router_casa_matriz-eth1 10.0.1.1 netmask 255.255.255.0')

# Crear el router de la Sucursal 1
router_sucursal1 = net.addHost('router_sucursal1')
router_sucursal1.cmd('ifconfig router_sucursal1-eth0 192.168.100.0 netmask 255.255.255.248')
router_sucursal1.cmd('ifconfig router_sucursal1-eth1 10.0.1.2 netmask 255.255.255.0')

# Crear el router de la Sucursal 2
router_sucursal2 = net.addHost('router_sucursal2')
router_sucursal2.cmd('ifconfig router_sucursal2-eth0 192.168.100.8 netmask 255.255.255.248')
router_sucursal2.cmd('ifconfig router_sucursal2-eth1 10.0.2.1 netmask 255.255.255.0')

# Crear los hosts de las sucursales
host_sucursal1 = net.addHost('host_sucursal1', ip='10.0.1.254/24')
host_sucursal2 = net.addHost('host_sucursal2', ip='10.0.2.254/24')

# Conectar los dispositivos de red
net.addLink(router_casa_matriz, router_sucursal1)
net.addLink(router_casa_matriz, router_sucursal2)
net.addLink(router_sucursal1, host_sucursal1)
net.addLink(router_sucursal2, host_sucursal2)

# Iniciar la red
net.start()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()