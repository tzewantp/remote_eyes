# This program can run on BeagleBone. It waits for a 4 bytes packet that begins with the start byte 0xAB.
# Packet scheme:
#     <Start Byte>, <Address - Always 0x01>, <Command Byte - 0x88>, <Sensor Data - Either 0x00 or 0x01>
# Future improvements: Use circular buffer scheme.

import serial
import time

mySerial = serial.Serial('/dev/ttyUSB0', 9600, timeout=3)
print("Connected to: " + mySerial.portstr)

recv = []
recv = [0 for i in range(10)]         # Array to store received data
bytes_read = 0                        # Counter to track number of bytes read
start_index = 0                       # Index into the array to point to start byte 

while True:
  if mySerial.InWaiting() > 0:
    my_byte_str = mySerial.read(1)    # Read 1 byte at a time. Returned type is 'char'
    recv[bytes_read] = ord(my_byte_str)  # ord() converts from 'char' to 'int'
    if (recv[bytes_read] == 0xAB):       # 0xAB is the start byte
      start_index = bytes_read        # Track start_index for start byte

    bytes_read = bytes_read + 1  
    
  if bytes_read >= 4:                 # When we have received a completed packet:
    start_index = 0                   # reset back to 0
    if (recv[start_index] == 0xAB and recv[start_index+1] == 0x01 and recv[start_index+2] == 0x88 and recv[start_index+1] == 0x01):
      print("PIR sensor on")
    elif (recv[start_index] == 0xAB and recv[start_index+1] == 0x01 and recv[start_index+2] == 0x88 and recv[start_index+1] == 0x00):
      print("PIR sensor on")
     
