from hal.eth import UdpComm
import time

class stepper():
    """
class to control steppers
    """

    def eventReceiver(self, message):
        print message

    def __init__(self, name, udp):
        self.stepper_name = name
        self.stepper_pos = 0
        self.UDP = udp

    def step(self, steps, direction, steps_per_sec):
        msg = "%s.steps:%i,%i,%i" % (self.stepper_name, steps, direction, steps_per_sec)
        self.UDP.send_udp(msg)
        self.stepper_pos = self.stepper_pos + (direction * steps)


    def set(self, position, direction, steps_per_sec):
        msg = "%s.set:%i,%i,%i" % (self.stepper_name, position, direction, steps_per_sec)
        self.UDP.send_udp(msg)
        self.stepper_pos = position

    def get(self):
        return self.stepper_pos