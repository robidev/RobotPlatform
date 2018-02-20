from hal.eth import UdpComm

class microphone():
    """
class to receive sound from microphone
    """
    self.HEADER = 4

    def __init__(self, IP="127.0.0.1"):
        self.ADDR = IP
        self.UDP = UdpComm("127.0.0.1",5000,5001)

    def listen(self, length):
        sound_buffer = []
        for i in range(length):
            sound_buffer.append(0)
        msg = "mic:%i" % length
        self.UDP.bind()
        self.UDP.send_udp(msg,self.ADDR)
        sound_buffer, addr = self.UDP.recv_udp(HEADER + length)
        return sound_buffer