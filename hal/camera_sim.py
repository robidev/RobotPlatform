from hal.eth import UdpComm
import zlib

class camera():
    """
class to receive images from a camera
    """
    def eventReceiver(self, message):
        print message

    def __init__(self,name, udp):
        self.name = name
        self.UDP = udp
        self.ImageChannel = UdpComm(self.UDP.UDP_IP_r,5002) #channel for image reception
        self.width = 320
        self.height = 320
        self.DEPTH = "RGBA"

    def get_pic(self):
        image_buffer, addr = self.ImageChannel.recv_udp(HEADER + RESOLUTION)
        return image_buffer

    def start(self, camera):
        self.ImageChannel.bind()
        msg = camera + ".getimage" # rec:0 means, keep sending until stopped        
        self.UDP.send_udp(msg)

    def stop(self,camera):
        msg = camera + ".rec_stop" # rec:1 means, send one pic        
        self.UDP.send_udp(msg)

    def snapshot(self, camera):
        pic = ""
        self.ImageChannel.bind()
        msg = camera + ".getimage" # rec:1 means, send one pic        
        self.UDP.send_udp(msg)
        data, addr = self.ImageChannel.recv_udp(65536)
        if addr[0] == self.UDP.UDP_IP_s:#is the data coming from the intended source
            for da in self.stream_gzip_decompress(data):
                pic = pic + da
        return pic

    def stream_gzip_decompress(self, stream):
        dec = zlib.decompressobj(32 + zlib.MAX_WBITS)  # offset 32 to skip the header
        for chunk in stream:
            rv = dec.decompress(chunk)
            if rv:
                yield rv
