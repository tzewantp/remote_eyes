/* Simple program to receive pulses at PA_12 of STM32Nucleo F042K6 */

#include "mbed.h"

#define XBEE_SEND_INTERVAL_SECS         15
#define XBEE_DESTN_ADDR_64BIT_HIGH      0x01234567UL
#define XBEE_DESTN_ADDR_64BIT_LOW       0x0000AAAAUL


Ticker statusTimer; // 1 sec timer for LED to indicate 'running' status
Serial usb(SERIAL_TX, SERIAL_RX); // SERIAL_TX = PA_2, SERIAL_TX = PA_15 - Use for debugging
Serial xbeeSerial(PA_9, PA_10); //
InterruptIn eventIn(PA_12); // capture the pulse input to this pin
DigitalOut statusLed(LED1); // indicate 'running' status
volatile int pulseCount = 0; // keep track of number of pulses
volatile int timerTicks = 0; // keep track of number of ticks

// Function prototype/forward declaration for ISR.
void event_irq_measure() {
    pulseCount++;
    if (pulseCount % 100 == 0) {
       //usb.printf("Detected pulse count: %d\n", pulse_count);
    }
}

// Timer event to toggle the status LED
void timer_one_sec() {
   statusLed = !statusLed;
   timerTicks++;
}

unsigned char xbee_packet_checksum(unsigned char *pktBuffer, int lenPkt)
{
    int cnt;
    int sumBytes = 0;

    for(cnt=0; cnt<lenPkt; cnt++)
        sumBytes += pktBuffer[cnt];          // Add up all the bytes

    return(0xFF - (unsigned char)(sumBytes & 0x00FF));
}

void xbee_send(int numPulses)
{
    int cnt, x, checksum;
    unsigned char payload[4];
    unsigned char addr_high[4];
    unsigned char addr_low[4];
    unsigned char packet[40];

    // Form the payload:
    payload[0] = (unsigned char)((numPulses >> 8) & 0x00FF);
    payload[1] = (unsigned char)((numPulses) & 0x00FF);
    payload[2] = 0;
    payload[3] = 0;

    // Form the packet:
    cnt = 0;
    packet[cnt] = 0x7E;     // start byte
    packet[cnt++] = 0x00;   // length field MSB
    packet[cnt++] = 0x0F;   // length field LSB
    packet[cnt++] = 0x00;   // API identifier
    packet[cnt++] = 0x01;   // Frame ID
    memcpy(&packet[cnt], addr_high, 4); // Destn addr MSB
    cnt += 4;
    memcpy(&packet[cnt], addr_low, 4);  // Destn addr LSB
    cnt += 4;
    packet[cnt++] = 0x00;   // Options
    memcpy(&packet[cnt], payload, 4); // Payload
    cnt += 4;
    checksum = xbee_packet_checksum(packet + 3, cnt);
    packet[cnt++] = checksum; // Checksum

    // Send the packet
    for(x=0; x<cnt; x++)
    {
        xbeeSerial.putc(packet[x]);
    }
}

int main() {
    statusTimer.attach(&timer_one_sec, 1.0); // Initialise the status LED timer
    usb.printf("Pulse counting program:\n");
    eventIn.rise(&event_irq_measure); // Initialise interrupt in detection on rising edge.
    pulseCount = 0; // Initialise count

    while (1) {
        if(timerTicks >= XBEE_SEND_INTERVAL_SECS)
        {
            xbee_send(pulseCount);
            usb.printf("Sent pulse count: %d\n", pulseCount);
            timerTicks = 0; // reset ticks
            pulseCount = 0; // reset pulse count
        }
        wait(1);
    }
}
