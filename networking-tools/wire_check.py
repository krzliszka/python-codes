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
    Description
    """