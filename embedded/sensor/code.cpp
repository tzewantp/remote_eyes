#include "mbed.h"
 
Serial pcPort(SERIAL_TX, SERIAL_RX);  // Serial port for debugging
Serial xbeePort(PB_6, PB_7);          // Serial port for XBee
 
// send the alarm on/off message
const unsigned char TestMsg[] = { 'T', 'e', 's', 't', '\r' };

void xbee_Send(unsigned char *writeBuffer, int writeLen)
{
    int len;
    
    for (len = 0; len < writeLen; len++)
        xbeePort.putc(writeBuffer[len]);
}

int main()
{
    pc.printf("XBee simulator program running....\n");
    
    while(1)
    {
        xbee_Send();
        wait(5);
    }
}

