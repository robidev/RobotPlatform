from hal.eth import UdpComm
from hal.eth import TcpComm

class eventProcessor():
    """
class to handle events
    """
    def __init__(self):
        self.queueList = null # list containing all queue's
        self.name.queue = null #queue that will contain events for a given name
        self.name.callbacks = null #list of callbacks that subscribed to a given name
        self.name.queue_semaphore = False


#add a callback to a list
    def subscribe(self, name, callback):
        self.name.callbacks.append(callback)

#remove a callback from a list
    def unsubscribe(self, name, callback):
        self.name.callbacks.remove(callback)

#this message can be called from any publisher
    def publish(self, name, MESSAGE):
        while self.name.queue_semaphore == True:
            wait
        self.name.queue_semaphore = True
        self.name.queue.append(MESSAGE)
        #publish message to eventqueue
        self.name.queue_semaphore = False


#this loop handles the events at a predetermined rate by sending it to all subscribers
    def eventLoop(self,PERIOD):
        while True:
            for name in queueList:
                processEvents(name)
            time.wait(PERIOD)

#process events for a specific queue
    def processEvents(self,name):
        if(self.name.queue.Count > 0):
            while self.name.queue_semaphore == True:
                wait
            self.name.queue_semaphore = True
            for callback in self.name.callbacks
                self.name.callbacks(self.name.queue[0]) #call each registered callback with this message
            self.name.queue.remove(0) # remove index 0, after it was send to all subscribers
            self.name.queue_semaphore = False


class eventProcessorUdp():
"""
class to handle UDP messages
"""
    def __init__(self):
        self.UDP = UDP()
        self.events = eventProcessor()
        #register udp callback to the publish function, so that all udp messages are added to the queue
        
    def addUdpListener(self, name, callback):
        self.events.subscribe(name,callback)

    def parseUdpMessage(self, MESSAGE):
        #parse name from message
        self.events.publish(name, MESSAGE_sub)


class eventProcessorTcp():
"""
class to handle TCP messages
"""
    def __init__(self):
        self.TCP = TCP()
        self.events = eventProcessor()
        #register tcp callback to the publish function, so that all tcp messages are added to the queue
        
    def addTcpListener(self, name, callback):
        self.events.subscribe(name,callback)

    def parseTcpMessage(self, MESSAGE):
        #parse name from message
        self.events.publish(name, MESSAGE_sub)

