from __future__ import absolute_import, division, print_function, unicode_literals

from hal.eth import UdpComm
import threading
import datetime

class battery():
    """
class to retrieve battery state
    """
    def eventReceiver(self, message):
        if message.startswith(self.battery_name + b":"):
            self.status = message + b" - " + str.encode(str(datetime.datetime.now()))
            self.Statusevent.set()

    def __init__(self, name, udp):
        self.battery_name = name
        self.UDP = udp
        self.Statusevent = threading.Event()
        self.status = b""

    def charge(self):
        self.Statusevent.clear()
        msg = b"%s.charge" % self.battery_name
        self.UDP.send_udp(msg)

        #wait for asynchronous callback with data
        if self.Statusevent.wait(10) != True:
            print(u"error: did not receive status within 10 seconds")
        return self.status
