from hal.eth import UdpComm

class audio():
    """
class to send sound to speaker
    """

    def __init__(self, IP="127.0.0.1"):
        self.ADDR = IP
        self.UDP = UdpComm("127.0.0.1",5000,5001)

    def send_pic(self, sound):
        msg = "snd:%s" % sound
        self.UDP.send_udp(msg,self.ADDR)

