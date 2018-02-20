import socket

class UdpComm():
    """
A class to manage UDP connections
    """
    def __init__(self, receive_IP='127.0.0.1', receive_Port=5000, send_Port=5001):
        self.UDP_IP_r = receive_IP
        self.UDP_PORT_r = receive_Port
        self.UDP_PORT_s = send_Port
        self.sock_out = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

    def bind(self):
        self.sock_in = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock_in.bind((self.UDP_IP_r, self.UDP_PORT_r))

    def send_udp(self, MESSAGE, UDP_IP):
        self.sock_out.sendto(MESSAGE, (UDP_IP, self.UDP_PORT_s))

    def recv_udp(self, BUFFER=1024):
        return self.sock_in.recvfrom(BUFFER) # buffer size is 1024 bytes


class TcpCommServer():
    """
A class to manage a TCP server
    """
    def __init__(self, receive_IP='127.0.0.1', receive_Port=5000):
        self.TCP_IP_r = receive_IP
        self.TCP_PORT_r = receive_Port
        self.sock_out = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # TCP

    def bind(self):
        self.sock_in = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # TCP
        self.sock_in.bind((self.TCP_IP_r, self.TCP_PORT_r))
        self.sock_in.listen(1)

    def send_tcp(self, MESSAGE, UDP_IP):
        self.sock_out.send(MESSAGE)

    def accept(self):
        return self.sock_in.accept()

    def recv_tcp(self, BUFFER=1024):
        return self.sock_in.recv(BUFFER) # buffer size is 1024 bytes


class TcpCommClient():
    """
A class to manage a TCP client
    """
    def __init__(self, IP='127.0.0.1', send_Port=5000):
        self.TCP_IP = IP
        self.TCP_PORT = send_Port
        self.sock_out = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # TCP

    def connect(self):
        self.sock_out.connect((TCP_IP, TCP_PORT))

    def send(self, MESSAGE):
        self.sock_out.send(MESSAGE)

    def recv(self, BUFFER=1024):
        return  self.sock_out.recv(BUFFER_SIZE)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock_out.close()


