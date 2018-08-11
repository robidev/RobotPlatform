from blinker import signal
import time

from hal.eth import UdpComm
from hal.servo_sim import servo
from hal.camera_sim import camera
from hal.stepper_sim import stepper
#from hal.car_sim import car

UDP = UdpComm("127.0.0.1",5001,"127.0.0.1",5000)


def udpParser(message):
    if message.startswith("id:"): #we are dealing with an identify-response
        message = message[3:] #strip the id:
        if message.startswith("car:"):
            #print "car"
            resp = message[4:]
            devicelist[resp] = message[:3]
        if message.startswith("cam:"):
            #print "camera"
            resp = message[4:]
            devicelist[resp] = [message[:3],camera(resp,UDP)]
        if message.startswith("stepper:"):
            #print "stepper"
            resp = message[8:]
            devicelist[resp] = [message[:7], stepper(resp,UDP)]
        if message.startswith("servo:"):
            #print "servo"
            resp = message[6:]
            devicelist[resp] = [message[:5], servo(resp,UDP)]
        if message.startswith("display:"):
            print "display"
        if message.startswith("speaker:"):
            print "speaker"
        if message.startswith("mic:"):
            print "microphone"
        if message.startswith("gpio:"):
            print "general purpose IO"
        if message.startswith("uart:"):
            print "uart"
        if message.startswith("battery:"):
            print "battery"
    else:
        for key,value in devicelist.items():
            if message.startswith(key):
                values[1].eventReceiver(message)

UDP.bind(-1)

udpreceiver = signal('udpPacket')
udpreceiver.connect(udpParser)

time.sleep(1)
devicelist = dict()
UDP.send_udp("all.identify")
time.sleep(1)
for keys,values in devicelist.items():
    print "%s = %s" % (keys, values[0])

time.sleep(1)
for keys,values in devicelist.items():
    if values[0] == 'servo':
        values[1].set(45)
        print "%s set to 45" % keys
        time.sleep(4)

time.sleep(4)
print "done!"