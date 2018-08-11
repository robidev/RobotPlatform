from hal.eth import UdpComm

class microphone():
    """
class to receive sound from microphone
    """
    def eventReceiver(self, message):
        print message

    def __init__(self, name, udp):
        self.mic_name = name
        self.UDP = udp

    def listen(self, length):
        sound_buffer = []
        for i in range(length):
            sound_buffer.append(0)
        msg = "%s.mic:%i" % (self.mic_name, length)
        self.UDP.send_udp(msg)

        #wait for async callback with data

        sound_buffer = message
        return sound_buffer