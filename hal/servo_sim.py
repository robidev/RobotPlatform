from __future__ import absolute_import, division, print_function, unicode_literals

from hal.eth import UdpComm
import threading

class servo():
    """
class to control servo's
    """
    def eventReceiver(self, message):
        if message == self.servo_name + b":OK":
            self.Ackevent.set()
            

    def __init__(self, name, udp):
        self.servo_name = name
        self.servo_pos = 0
        self.UDP = udp
        self.Ackevent = threading.Event()

    def set(self, position):
        self.Ackevent.clear()
        msg = b"%s.servo:%i" % (self.servo_name, position)
        self.UDP.send_udp(msg)
        self.servo_pos = position

        #synchronous wait to async response
        if self.Ackevent.wait(10) != True:
            print(u"error: did not receive OK within 10 seconds")
        else:
            print(u"OK received")

    def get(self):
        return self.servo_pos

