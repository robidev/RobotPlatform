from hal.eth import UdpComm
import time

class servo():
    """
class to control servo's
    """
    def __init__(self, count, IP="127.0.0.1"):
        self.ADDR = IP
        self.servo_list = []
        self.servo_namelist = []
        for i in range(count):
            self.servo_list.append(0)
        self.UDP = UdpComm("127.0.0.1",5001,5000)

    def identify(self, TIMEOUT = 10):
        start = time.time()
        self.UDP.bind()
        self.UDP.send_udp("all.identify","127.0.0.1")
        while True:
            resp, addr = self.UDP.recv_udp(1024)
            if resp == 'identify:done':
                break
            if resp.startswith("servo:"):
                resp = resp[6:]
                self.servo_namelist.append(resp)
            end = time.time()
            timeout = end - start
            #print "time:%s" % timeout
            if timeout > TIMEOUT:
                break

    def set(self, index, position):
        msg = "%s.servo:%i" % (self.servo_namelist[index], position)
        self.UDP.send_udp(msg,self.ADDR)
        self.servo_list[index] = position

    def set_by_name(self, name, position):
        msg = "%s.servo:%i" % (name, position)
        self.UDP.send_udp(msg,self.ADDR)
        try:
            index = self.servo_namelist.index(name)
            self.servo_list[index] = position
        except ValueError:
            self.servo_namelist.append(name)
            index = self.servo_namelist.index(name)
            self.servo_list[index] = position

    def get(self, index):
        return self.servo_list[index]

    def get_by_name(self, name):
        index = self.servo_namelist.index(name)
        return self.servo_list[index]
