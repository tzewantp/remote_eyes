import serial
 
mySerial = serial.Serial('COM7', 9600)
buffer = [0 for i in range(100)]         # Array to store received data
bytes_read = 0                           # Counter to track number of bytes read
start_index = -1                         # Index into the array to point to start byte
packet_cnt = 0
 
while True:
    if (mySerial.in_waiting > 0):
    cnt = 0
    while (cnt < mySerial.in_waiting):
        my_byte_str = mySerial.read(1)         # Read 1 byte at a time. Returned type is 'char'
        buffer[bytes_read] = ord(my_byte_str)  # ord() converts from 'char' to 'int'
        if (buffer[bytes_read] == 0x7E):       # 0x7E is the start byte
            start_index = bytes_read           # Track start_index for start byte
            print 'start_index found at %d' % start_index
        bytes_read = bytes_read + 1  
        cnt = cnt + 1
    
    if (start_index is not -1):
        packet_cnt = packet_cnt + cnt
        if (packet_cnt >= 20):
            print 'Packet is found'
            start_index = -1
            packet_cnt = 0
            bytes_read = 0
