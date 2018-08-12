from __future__ import absolute_import, division, print_function, unicode_literals

from hal.eth import UdpComm
import zlib

class video():
    """
class to send images to display
    """
    def eventReceiver(self, message):
        print(message)

    def __init__(self, name, udp):
        self.display_name = name
        self.UDP = udp

    def send_frame(self, image):
        msg = b"%s.frame:%s" % (self.display_name, zlib.compress(image))
        self.UDP.send_udp(msg)

