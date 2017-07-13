import serial

mySerial = None
#mySerial = serial.Serial('COM7', 9600)
buffer = [0 for i in range(100)]            # Array to store received data
complete_xbee_pkt = [0 for i in range(30)]  # Array to store complete packet
bytes_read = 0                              # Counter to track number of bytes read
start_index = -1                            # Index into the array to point to start byte
packet_bytes = 0                            # Number of bytes received   

# Function to allow caller to set the serial port object
def set_serial_port(pserial):
    global mySerial 
    mySerial = pserial
    global bytes_read
    bytes_read = 0
    global start_index
    start_index = -1
    global packet_bytes
    packet_bytes = 0     
     
def check_packet():
    #print 'check packet called'
    global mySerial
    global bytes_read
    global start_index 
    global packet_bytes
    global buffer
    global complete_xbee_pkt
    
    bytes_in_waiting = mySerial.in_waiting
    if (bytes_in_waiting > 0):
        print 'Total bytes to read is %d' % bytes_in_waiting    
        cnt = 0
        while (cnt < bytes_in_waiting):
            # .read(size = 1):
            # Read size bytes from the serial port. If a timeout is set it may 
            # return less characters as requested. With no timeout it will block 
            # until the requested number of bytes is read.
            # Changed in version 2.5: Returns an instance of bytes when available 
            # (Python 2.6 and newer) and str otherwise.        
            my_byte_str = mySerial.read(1)         # Read 1 byte at a time. Returned type is 'char'
            buffer[bytes_read] = ord(my_byte_str)  # ord() converts from 'char' to 'int'
            if (start_index is -1):
                if (buffer[bytes_read] == 0x7E):       # 0x7E is the start byte
                    start_index = bytes_read           # Track start_index for start byte
                    print '->start_index found at %d' % start_index
            bytes_read = bytes_read + 1  
            cnt = cnt + 1
            
        if (start_index is not -1):                    # Means that start byte is found.
            packet_bytes = packet_bytes + cnt
            if (packet_bytes > 3):
                packet_len = (buffer[start_index + 1] << 8) + buffer[start_index + 2] 
                packet_len += 4                     # Add 4 bytes (First 3 bytes + checksum)
                print '->Packet len is %d' % packet_len
                if (packet_bytes >= packet_len):
                    print '->Packet is found'
                    # Copy out the packet
                    for x in range(packet_len):
                        complete_xbee_pkt[x] = buffer[start_index + x]
                
                    start_index = -1
                    packet_bytes = 0
                    bytes_read = 0
                    return True
    return False

def get_command():
    print '..get command'
    return 10
 
def get_data():
    print '..get data'
    global complete_xbee_pkt
    data = complete_xbee_pkt[14]
    return data
 
