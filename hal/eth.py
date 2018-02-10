import socket

class UdpComm():
    """
A class to manage UDP connections
    """
    def __init__(self, receive_IP='127.0.0.1', receive_Port=5000, send_Port=5000):
        self.UDP_IP_r = receive_IP
        self.UDP_PORT_r = receive_Port
        self.UDP_PORT_s = send_Port
        self.sock_out = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        #self.sock_in = socket.socket(socket.AF_INET, # Internet
        #             socket.SOCK_DGRAM) # UDP
        #self.sock_in.bind((self.UDP_IP_r, self.UDP_PORT_r))


    def send_udp(self, MESSAGE, UDP_IP):
        self.sock_out.sendto(MESSAGE, (UDP_IP, self.UDP_PORT_s))


    def recv_udp(self, BUFFER=1024):
        return self.sock_in.recvfrom(BUFFER) # buffer size is 1024 bytes

