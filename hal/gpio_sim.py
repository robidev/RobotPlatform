from hal.eth import UdpComm

class gpio():
    """
class to get/set gpio states
    """

    def __init__(self, IP="127.0.0.1"):
        self.ADDR = IP
        self.UDP = UdpComm("127.0.0.1",5000,5001)
