from hal.eth import UdpComm

class stepper():
    """
class to control steppers
    """
    def __init__(self, count, IP="127.0.0.1"):
        self.ADDR = IP
        self.stepper_list = []
        for i in range(count):
            self.stepper_list.append(0)
        self.UDP = UdpComm("127.0.0.1",5000,5001)

    def set(self, index, position, direction, speed):
        msg = "step_pos:%i,%i,%i,%i" % (index, position, direction, speed)
        self.UDP.send_udp(msg,self.ADDR)
        self.stepper_list[index] = position

    def step(self, index, direction, steps, speed):
        msg = "stepper:%i,%i,%i,%i" % (index, direction, steps, speed)
        self.UDP.send_udp(msg,self.ADDR)
        self.stepper_list[index] = -1

    def get(self, index):
        return self.stepper_list[index]