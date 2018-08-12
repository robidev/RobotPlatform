from __future__ import absolute_import, division, print_function, unicode_literals

from hal.eth import UdpComm
import threading
import time

class car():
    """
class to control the car
    """
    def eventReceiver(self, message):
        if message.startswith(self.car_name + ":"):
            print(message)

    def __init__(self, name, udp):
        self.car_name = name
        self.UDP = udp

    def forward(self):
        msg = b"%s.forward" % self.car_name
        self.UDP.send_udp(msg)

    def back(self):
        msg = b"%s.back" % self.car_name
        self.UDP.send_udp(msg)

    def stop(self):
        msg = b"%s.stop" % self.car_name
        self.UDP.send_udp(msg)


