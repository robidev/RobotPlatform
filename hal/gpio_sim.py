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
        self.status = ""

    def get(self, GPIO_port):
        self.Statusevent.clear()
        msg = "%s.get:%s" % (self.gpio_name, GPIO_port)
        self.UDP.send_udp(msg)

        #wait for async callback with data
        if self.Statusevent.wait(10) != True:
            self.status = "error: did not receive status within 10 seconds"
        return self.status

    def set(self, GPIO_port, state):
        msg = "%s.set:%s=%s" % (self.gpio_name, GPIO_port, state)
        self.UDP.send_udp(msg)