from hal.eth import UdpComm
import zlib

class camera():
    """
class to receive images from a camera
    """

    def __init__(self, IP="127.0.0.1"):
        self.ADDR = IP
        self.UDP = UdpComm("127.0.0.1",5002,5000)
        self.width = 320
        self.height = 320
        self.DEPTH = "RGBA"

    def get_pic(self):
        image_buffer, addr = self.UDP.recv_udp(HEADER + RESOLUTION)
        return image_buffer

    def start(self, camera):
        self.UDP.bind()
        msg = camera + ".getimage" # rec:0 means, keep sending until stopped        
        self.UDP.send_udp(msg,self.ADDR)

    def stop(self,camera):
        msg = camera + ".rec_stop" # rec:1 means, send one pic        
        self.UDP.send_udp(msg,self.ADDR)

    def snapshot(self, camera):
        pic = ""
        self.UDP.bind()
        msg = camera + ".getimage" # rec:1 means, send one pic        
        self.UDP.send_udp(msg,self.ADDR)
        data, addr = self.UDP.recv_udp(65536)
        if addr[0] == self.ADDR:
            for da in self.stream_gzip_decompress(data):
                pic = pic + da
        return pic

    def stream_gzip_decompress(self, stream):
        dec = zlib.decompressobj(32 + zlib.MAX_WBITS)  # offset 32 to skip the header
        for chunk in stream:
            rv = dec.decompress(chunk)
            if rv:
                yield rv
