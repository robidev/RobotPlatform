#!/usr/bin/env python
import time
from hal.eth import UdpComm

UDP = UdpComm()
UDP.send_udp("hello world1","192.168.192.1")
UDP.send_udp("hello world2","127.0.0.1")
UDP.send_udp("forward","127.0.0.1")

time.sleep(1)
UDP.send_udp("back","127.0.0.1")

time.sleep(1)

UDP.send_udp("forward","127.0.0.1")

time.sleep(1)

UDP.send_udp("stop","127.0.0.1")

#data, addr = UDP.recv_udp()
#print "received '" +  data + "' from '" + addr[0] + ":" + str(addr[1]) + "'"
