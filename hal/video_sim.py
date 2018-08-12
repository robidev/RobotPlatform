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
        #zlib_encode = zlib.compressobj(6, zlib.DEFLATED, zlib.MAX_WBITS | 16)
        #content = zlib_encode.compress(image) + zlib_encode.flush()

        """
        pic = b""
        for da in self.stream_gzip_decompress(content):
            pic = pic + da
        print(pic)
        """

        msg = b"%s.frame:%s" % (self.display_name, image)#content)
        self.UDP.send_udp(msg)

"""
    def stream_gzip_decompress(self, stream):
        dec = zlib.decompressobj(32 + zlib.MAX_WBITS)  # offset 32 to skip the header

        rv = dec.decompress(stream)
        if rv:
            yield rv
"""