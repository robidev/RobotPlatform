from hal.eth import UdpComm

class battery():
    """
class to retrieve battery state
    """
    self.HEADER = 4

    def __init__(self, IP="127.0.0.1"):
        self.ADDR = IP
        self.UDP = UdpComm("127.0.0.1",5000,5001)

    def charge(self):
        self.UDP.bind()
        self.UDP.send_udp("charge",self.ADDR)
        return self.UDP.recv_udp(HEADER + length)

