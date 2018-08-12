from __future__ import absolute_import, division, print_function, unicode_literals

from hal.eth import UdpComm

class audio():
    """
class to send sound to speaker
    """
    def eventReceiver(self, message):
        print(message)

    def __init__(self, name, udp):
        self.speaker_name = name
        self.UDP = udp

    def send_sound(self, sound):
        msg = b"%s.snd:%s" % (self.speaker_name, sound)
        self.UDP.send_udp(msg)

