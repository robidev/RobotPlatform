from __future__ import absolute_import, division, print_function, unicode_literals

from hal.eth import UdpComm
import threading
import time

class gpio():
    """
class to get/set gpio states
    """
    def eventReceiver(self, message):
        if message.startswith(self.gpio_name + ":"):
            self.status = message + " - " + time.time()
            self.Statusevent.set()

    def __init__(self, name, udp):
        self.gpio_name = name
        self.UDP = udp
        self.Statusevent = threading.Event()
        self.status = u""

    def get(self, GPIO_port):
        self.Statusevent.clear()
        msg = b"%s.get:%s" % (self.gpio_name, GPIO_port)
        self.UDP.send_udp(msg)

        #wait for async callback with data
        if self.Statusevent.wait(10) != True:
            self.status = u"error: did not receive status within 10 seconds"
        return self.status

    def set(self, GPIO_port, state):
        msg = b"%s.set:%s=%s" % (self.gpio_name, GPIO_port, state)
        self.UDP.send_udp(msg)
