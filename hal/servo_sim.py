from hal.eth import UdpComm

class servo():
    """
class to control servo's
    """
    def __init__(self, count, IP="127.0.0.1"):
        self.ADDR = IP
        self.servo_list = []
        for i in range(count):
            self.servo_list.append(0)
        self.UDP = UdpComm("127.0.0.1",5000,5001)

    def set(self, index, position):
        msg = "servo:%i,%i" % (index, position)
        self.UDP.send_udp(msg,self.ADDR)
        self.servo_list[index] = position

    def get(self, index):
        return self.servo_list[index]