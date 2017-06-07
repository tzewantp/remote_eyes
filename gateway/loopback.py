#!/usr/bin/python
#
# This test program demonstrates a loopback test
# using the PySerial.
# It can be used for testing while the device is
# not ready.
#
import threading
import serial
import time

def serialDataPump():
    testCtr = 0;
    elements=[0x41, 0x42, 0x43, 0x44, 0x0A]         #is this a dic?
    send_array = bytearray(elements)  #create byte array
    while True:
        #ser.write(bytes("Test\n"))
        ser.write(bytes(send_array))
        time.sleep(1)
        testCtr += 1
        
 
def serialDataTestRcv():
    while True:
        line = ser.readline()
        print 'received ' + str(line)
    
ser = serial.serial_for_url('loop://', timeout=1)
      
thread1 = threading.Thread(target = serialDataPump)
thread2 = threading.Thread(target = serialDataTestRcv)
thread1.start()
thread2.start()
thread1.join()
exit()
