#!/usr/bin/env python

"""
TODO:
make unity-sim for gpio and display
make battery unity-sim
make audio and mic unity-sim
test and extend car unity-sim

missing: uart, storage(internal) and timer(internal)

next: make interactive webpage for easy control/access and scripting of behavior
use flask, (with websockets?)

"""

from blinker import signal
import time
from PIL import Image

from hal.eth import UdpComm
from hal.servo_sim import servo
from hal.camera_sim import camera
from hal.stepper_sim import stepper
from hal.video_sim import video
from hal.audio_sim import audio
from hal.mic_sim import microphone
from hal.gpio_sim import gpio
from hal.battery_sim import battery
from hal.car_sim import car

#function to handle signals from the UDP receiver
def udpParser(message):
    if message.startswith("id:"): #we are dealing with an identify-response that lists all the connected devices
        message = message[3:] #strip the id:
        if message.startswith("car:"):
            resp = message[4:]
            devicelist[resp] = [message[:3], car(resp,UDP)]
        if message.startswith("cam:"):
            resp = message[4:]
            devicelist[resp] = [message[:3], camera(resp,UDP)]
        if message.startswith("stepper:"):
            resp = message[8:]
            devicelist[resp] = [message[:7], stepper(resp,UDP)]
        if message.startswith("servo:"):
            resp = message[6:]
            devicelist[resp] = [message[:5], servo(resp,UDP)]
        if message.startswith("display:"):
            resp = message[8:]
            devicelist[resp] = [message[:7], video(resp,UDP)]
        if message.startswith("speaker:"):
            resp = message[8:]
            devicelist[resp] = [message[:7], audio(resp,UDP)]
        if message.startswith("mic:"):
            resp = message[4:]
            devicelist[resp] = [message[:3], microphone(resp,UDP)]
        if message.startswith("gpio:"):
            resp = message[5:]
            devicelist[resp] = [message[:4], gpio(resp,UDP)]
        if message.startswith("battery:"):
            resp = message[8:]
            devicelist[resp] = [message[:7], battery(resp,UDP)]
    elif message == 'identify:done':#we are done with the identify request
        for key,value in devicelist.items():
            print "%s = %s" % (key, value[0])#print all the found devices

    else:#forward the message to the intended device for further processing
        for key,value in devicelist.items():
            if message.startswith(key + ':'):
                value[1].eventReceiver(message)



#set up a UDP connection to our robot
UDP = UdpComm("127.0.0.1",5001,"127.0.0.1",5000)

UDP.bindAsync(-1) #listen asynchronous with no timeout
udpreceiver = signal('udpPacket') # register to the signals coming from the udp listener
udpreceiver.connect(udpParser) #connect the parser as a callback

time.sleep(1)

#identify all components in the robot, response is in callback
devicelist = dict()
UDP.send_udp("all.identify")


#set some values of the robot components
time.sleep(1)
for keys,values in devicelist.items():
    if values[0] == 'servo':
        values[1].set(45)
        print "%s set to 45" % keys
        
    if values[0] == 'stepper':
        values[1].set(25,-1,10)
        print "%s set to 25" % keys

    if values[0] == 'cam':
        picture = values[1].snapshot()
        if len(picture) > 0:
            Image.frombytes(values[1].DEPTH,(values[1].width, values[1].height),picture).transpose(Image.FLIP_TOP_BOTTOM).show()
        else:
            print "could not get snapshot"

    if values[0] == 'display':
        img = Image.frombytes('RGBA',(10,1),"testaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbba")
        values[1].send_frame(img)

    time.sleep(2)




time.sleep(4)
print "done!"