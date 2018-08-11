from hal.eth import UdpComm
import threading
import time

class battery():
    """
class to retrieve battery state
    """
    def eventReceiver(self, message):
        if message.startswith(self.battery_name + ":"):
            self.status = message + " - " + time.time()
            self.Statusevent.set()

    def __init__(self, name, udp):
        self.battery_name = name
        self.UDP = udp
        self.Statusevent = threading.Event()
        self.status = ""

    def charge(self):
        self.Statusevent.clear()
        msg = "%s.charge" % self.battery_name
        self.UDP.send_udp(msg)

        #wait for asynchronous callback with data
        if self.Statusevent.wait(10) != True:
            print "error: did not receive status within 10 seconds"
        return self.status
