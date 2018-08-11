from hal.eth import UdpComm
import time

class servo():
    """
class to control servo's
    """
    def eventReceiver(self, message):
        print message

    def __init__(self, name, udp):
        self.servo_name = name
        self.servo_pos = 0
        self.UDP = udp

    def set(self, position):
        msg = "%s.servo:%i" % (self.servo_name, position)
        self.UDP.send_udp(msg)
        self.servo_pos = position

    def get(self):
        return self.servo_pos

