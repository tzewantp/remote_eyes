#!/usr/bin/python

import threading
import Queue
import time

# ============================================================================
# Create thread that writes to queue
# To implement a new thread using the threading module:
# 1. Define a new subclass of the Thread class.
# 2. Override the __init__(self [,args]) method to add additional arguments.
# 3. Override the run(self [,args]) method to implement what the thread should
#    do when started.
# Reference: https://www.tutorialspoint.com/python/python_multithreading.htm
# ============================================================================

# Define subclass of thread that listens for data and writes to queue:
class myListenThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "Starting " + self.name
        listen_xbee(self.name)
        print "Exiting " + self.name

# Define subclass of thread that fetches data from queue:
class myPublishMqttThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "Starting " + self.name
        insert_mqtt(self.name)
        print "Exiting " + self.name

# Define thread function that listen to xbee:
def listen_xbee(threadName):
    value = 1
    while True:
        msg_queue.put(value)
        print "inserted:", value
	value += 1	
        time.sleep(3)

# Define thread function that publish MQTT message: 
def insert_mqtt(threadName):
    while True:
        while not msg_queue.empty():
            print "fetched:", msg_queue.get()


# Create the queue
msg_queue = Queue.Queue()

# Create the threads
listenThread = myListenThread(1, "Listen Thread")
mqttPubThread = myPublishMqttThread(2, "MQTT Thread")

# Start the threads
listenThread.start()
mqttPubThread.start()

# Wait for the threads to complete (which does not happen)
listenThread.join()
mqttPubThread.join()
print "Exiting main thread"
