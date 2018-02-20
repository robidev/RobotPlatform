from hal.eth import UdpComm

class video():
    """
class to send images to display
    """

    def __init__(self, IP="127.0.0.1"):
        self.ADDR = IP
        self.UDP = UdpComm("127.0.0.1",5000,5001)

    def send_pic(self, image):
        msg = "vid:%s" % image
        self.UDP.send_udp(msg,self.ADDR)


