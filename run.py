#!/usr/bin/env python
import time
#import Image
from hal.eth import UdpComm
from hal.servo_sim import servo
from hal.camera_sim import camera

s = servo(3)
#s.identify()
#s.set(0,45)
time.sleep(1)
s.set_by_name("Arm3",0)
time.sleep(1)
s.set_by_name("Arm3",45)
#s.set(1,5)
#s.set(2,6)

#print "servo %i" % s.get(0)
#print "servo %i" % s.get(1)
#print "servo %i" % s.get(2)

#cam = camera()
#picture = cam.snapshot("all")
#if len(picture) > 0:
#    Image.frombytes(cam.DEPTH,(cam.width, cam.height),picture).transpose(Image.FLIP_TOP_BOTTOM).show()
#else:
#    print "could not get snapshot"



#UDP = UdpComm("127.0.0.1",5001,5000)
#time.sleep(1)
#UDP.send_udp("all.identify","127.0.0.1")
#time.sleep(1)
#UDP.send_udp("all.servo:0","127.0.0.1")

