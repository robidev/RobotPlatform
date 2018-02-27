from hal.eth import UdpComm
import time

class stepper():
    """
class to control steppers
    """
    def __init__(self, count, IP="127.0.0.1"):
        self.ADDR = IP
        self.stepper_list = []
        self.stepper_namelist = []
        for i in range(count):
            self.stepper_list.append(0)
        self.UDP = UdpComm("127.0.0.1",5001,5000)

    def identify(self, TIMEOUT = 10):
        start = time.time()
        self.UDP.bind()
        self.UDP.send_udp("all.identify","127.0.0.1")
        while True:
            resp, addr = self.UDP.recv_udp(1024)
            if resp == 'identify:done':
                break
            if resp.startswith("stepper:"):
                resp = resp[8:]
                self.stepper_namelist.append(resp)
            end = time.time()
            timeout = end - start
            #print "time:%s" % timeout
            if timeout > TIMEOUT:
                break

    def step(self, index, steps, direction, steps_per_sec):
        msg = "%s.steps:%i,%i,%i" % (self.stepper_namelist[index], steps, direction, steps_per_sec)
        self.UDP.send_udp(msg,self.ADDR)
        self.stepper_list[index] = -1 #steps=-1 means keep steppin, x>0 means take x steps

    def step_by_name(self, name, steps, direction, steps_per_sec):
        msg = "%s.steps:%i,%i,%i" % (name, steps, direction, steps_per_sec)
        self.UDP.send_udp(msg,self.ADDR)
        try:
            index = self.stepper_namelist.index(name)
            self.stepper_list[index] = -1
        except ValueError:
            self.stepper_namelist.append(name)
            index = self.stepper_namelist.index(name)
            self.stepper_list[index] = -1

    def set(self, index, position, direction, steps_per_sec):
        msg = "%s.set:%i,%i,%i" % (self.stepper_namelist[index], position, direction, steps_per_sec)
        self.UDP.send_udp(msg,self.ADDR)
        self.stepper_list[index] = position

    def set_by_name(self, name, position, direction, steps_per_sec):
        msg = "%s.set:%i,%i,%i" % (name, position, direction, steps_per_sec)
        self.UDP.send_udp(msg,self.ADDR)
        try:
            index = self.stepper_namelist.index(name)
            self.stepper_list[index] = position
        except ValueError:
            self.stepper_namelist.append(name)
            index = self.stepper_namelist.index(name)
            self.stepper_list[index] = position

    def get(self, index):
        return self.stepper_list[index]

    def get_by_name(self, name):
        index = self.stepper_namelist.index(name)
        return self.stepper_list[index]