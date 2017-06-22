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

# explicit import for py2exe - to fix "loop://" url issue 
#import serial.urlhandler.protocol_loop

def serialDataPump():
    print 'Started Sending Thread'
    header = [0x7E, 0x00, 0x0F, 0x00, 0x01]   # This is a list
    mac64addr = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
    options = [0x00]
    data = [0x00, 0x00, 0x00, 0x00]
     
    # Join the list to form the packet with the checksum byte not calculated yet.
    packet = header + mac64addr + options + data  
    
    # Calculate the checksum byte. Exclude first 3 bytes.
    checksum_byte = 0
    for i in range(len(packet)):
        if(i > 2):
            checksum_byte += packet[i] 

    # Take only the lowest 8 bits
    checksum_byte = 0x00FF & checksum_byte

    # Add one more byte to the list
    packet += []
    
    # Subtract from 0xFF
    packet[len(packet) - 1] = 0xFF - checksum_byte

    send_array = bytearray(packet)  #create byte array
    while True:
        #ser.write(bytes("Test\n"))
        ser.write(bytes(send_array))
        time.sleep(1)
        
 
def serialDataTestRcv():
    print 'Started Receiving Thread'
    while True:
        line = ser.read(19)
        print 'received ' + str(line)
    
ser = serial.serial_for_url('loop://', timeout=1)
      
thread1 = threading.Thread(target = serialDataPump)
thread2 = threading.Thread(target = serialDataTestRcv)
thread1.start()
thread2.start()
thread1.join()
exit()
