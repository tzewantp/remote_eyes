#!/usr/bin/python

import threading
import Queue
import time
import serial
import receive
import mqtt_client
 
 
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
        print "Starting: " + self.name
        listen_xbee(self.name)
        print "Exiting " + self.name

# Define subclass of thread that fetches data from queue:
class myPublishMqttThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "Starting: " + self.name
        insert_mqtt(self.name)
        print "Exiting " + self.name

# Define subclass of thread that simulates sending of data:
class mySimXbeeNode (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "Starting: " + self.name
        simulate_xbee_node_sending(self.name)
        print "Exiting " + self.name
        
# Start Serial Port
def init_serial(ser, simSend):

    if(simSend == True):
        # Create thread that simulates the Xbee node sending
        xbeeSendThread = mySimXbeeNode(1, "Simulate XBee Send Thread")
        xbeeSendThread.start()  
        
    # Pass the serial port instance to the receive module
    receive.set_serial_port(ser)

# Sending Data
def simulate_xbee_node_sending(threadName):
    header = [0x00, 0x7E, 0x00, 0x0F, 0x00, 0x01]   # This is a list
    mac64addr = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
    options = [0x00]
    data = [0x00, 0x00, 0x00, 0x00]
    checksum = [0x00]   # Arbitrary checksum
    
    while True:
        if(data[1] < 255):
            data[1] += 1
        else:
            data[1] = 0

        # Join the list to form the packet with the checksum byte not calculated yet.
        packet = header + mac64addr + options + data + checksum
    
        # Calculate the checksum byte. Exclude first 3 bytes.
        checksum_byte = 0
        for i in range(len(packet)):
            if(i > 3):
                checksum_byte += packet[i] 

        # Take only the lowest 8 bits
        checksum_byte = 0x00FF & checksum_byte
   
        # Subtract from 0xFF
        packet[len(packet) - 1] = 0xFF - checksum_byte

        # Convert to bytearray
        send_array = bytearray(packet)  
        #ser.write(bytes("Test\n"))
        
        # .write(data): 
        # Write the bytes data to the port. This should be of type bytes 
        # (or compatible such as bytearray or memoryview). Unicode strings 
        # must be encoded (e.g. 'hello'.encode('utf-8'). Changed in version 
        # 2.5: Accepts instances of bytes and bytearray when available 
        # (Python 2.6 and newer) and str otherwise.
        bwritten = ser.write(bytes(send_array))
        print "Bytes sent = " + str(bwritten)
        time.sleep(5)
        
        
# Define thread function that listens to xbee:
def listen_xbee(threadName):
    while True:
        if receive.check_packet() == True:
            xbeeCmd = receive.get_command()
            xbeeData = receive.get_data()
            msg_queue.put(xbeeData)
            #print(line)

        
# Define thread function that publishes MQTT message: 
def insert_mqtt(threadName):
    while True:
        while not msg_queue.empty():
            data = msg_queue.get()
            mqtt_client.publish_msg(data)


if __name__ == "__main__":
    print("main.py is being run")

    global ser 
    simulateSending = False   

    if(simulateSending == True):    
        ser = serial.serial_for_url('loop://')
    else:
        #ser = serial.Serial('COM5', 9600)
        ser = serial.Serial('/dev/ttyUSB1', 9600)
        
    # Create the queue
    msg_queue = Queue.Queue()

    # Start the serial port
    init_serial(ser, simulateSending)
    
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
