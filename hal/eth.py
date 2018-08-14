from __future__ import absolute_import, division, print_function, unicode_literals

import socket
import threading
import time
from blinker import signal
import queue
import asyncore

def udpParser(message):
    pass

def udpReceiver_thread( threadName, udp):
    start = time.time()
    while True:
        try:
            resp, addr = udp.recv_udp(1024,1)
            udp.udpreceiver.send(resp)
        except udp.TimeoutError:
            print(u"socket timeout")        

        end = time.time()
        timeout = end - start
        if timeout > udp.TIMEOUT and udp.TIMEOUT != -1:
            print(u"UDP receiver thread timed out")
            break


class UdpComm():
    """
A class to manage UDP connections
    """
    class TimeoutError(Exception):
        pass

    def __init__(self, receive_IP='127.0.0.1', receive_Port=5000, send_IP='127.0.0.1', send_Port=5001 ):
        self.UDP_IP_r = receive_IP
        self.UDP_IP_s = send_IP
        self.UDP_PORT_r = receive_Port
        self.UDP_PORT_s = send_Port
        self.sock_out = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

    #the synchronous udp receiver)
    def bind(self):
        self.sock_in = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock_in.bind((self.UDP_IP_r, self.UDP_PORT_r))


    #the asynchronous udp receiver threat will run until 'TIMEOUT' (default is 10 seconds)
    def bindAsync(self,TIMEOUT = 10):
        self.TIMEOUT = TIMEOUT
        self.udpreceiver = signal('udpPacket')
        self.udpreceiver.connect(udpParser)

        self.sock_in = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock_in.bind((self.UDP_IP_r, self.UDP_PORT_r))
        try:
            threading.Thread( target=udpReceiver_thread, args=("udpReceiver_thread", self,) ).start()
        except:
            print(u"Error: unable to start thread")

    def send_udp(self, MESSAGE):
        self.sock_out.sendto(MESSAGE, (self.UDP_IP_s, self.UDP_PORT_s))

    #TIMEOUT_sock defines the time in seconds before the socket times out when no data is received
    def recv_udp(self, BUFFER=1024, TIMEOUT_sock=-1):
        if TIMEOUT_sock != -1:
            self.sock_in.settimeout(TIMEOUT_sock)

        try:
            return self.sock_in.recvfrom(BUFFER) # buffer size is 1024 bytes
        except socket.timeout:
            raise self.TimeoutError(u"UDP receiver timed out") 


class TcpCommServer(asyncore.dispatcher):
    """
A class to manage a TCP server
    """
    def __init__(self, receive_IP='127.0.0.1', receive_Port=4000):
        asyncore.dispatcher.__init__(self)
        self.TCP_IP_r = receive_IP
        self.TCP_PORT_r = receive_Port
        #self.sock_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((receive_IP, receive_Port))
        self.listen(1)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print(u'Incoming connection from %s' % repr(addr))
            handler = EchoHandler(sock)

    def bind(self):
        self.sock_in = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # TCP
        self.sock_in.bind((self.TCP_IP_r, self.TCP_PORT_r))
        self.sock_in.listen(1)

    def loop_tcp(self):
        return asyncore.loop()

    class EchoHandler(asyncore.dispatcher_with_send):

        def handle_read(self):
            data = self.recv(65530)
            if data:
                self.send(data)


def tcpParser(message):
    pass

class TcpCommClient(asyncore.dispatcher):
    """
A class to manage a TCP client
needs asyncore.loop() to work
    """
    def __init__(self, IP='127.0.0.1', Port=4000):
        asyncore.dispatcher.__init__(self)
        self.TCP_IP = IP
        self.TCP_PORT = Port

        self.tcpreceiver = signal('TcpPacket')
        self.tcpreceiver.connect(tcpParser)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (self.TCP_IP, self.TCP_PORT) )
        self.buf = queue.Queue()
        self.send_buf = b''
        self.TIMEOUT = -1

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        resp = self.recv(65530)
        self.tcpreceiver.send(resp)

    def writable(self):
        if not self.buf.empty():
            self.send_buf = self.buf.get()
        return (len(self.send_buf) > 0)

    def handle_write(self):
        sent = self.send(self.send_buf)
        self.send_buf = self.send_buf[sent:]

    def send_tcp(self, MESSAGE):
        self.buf.put(MESSAGE)

    def send_udp(self, MESSAGE):
        self.buf.put(MESSAGE)
