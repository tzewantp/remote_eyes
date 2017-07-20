/* Simple program to receive pulses at PA_12 of STM32Nucleo F042K6 */

#include "mbed.h"

#define XBEE_SEND_INTERVAL_SECS         15
#define XBEE_DESTN_ADDR_64BIT_HIGH      0x0013A200UL
#define XBEE_DESTN_ADDR_64BIT_LOW       0x41528AFDUL


Ticker statusTimer; // 1 sec timer for LED to indicate 'running' status
Ticker simPulseOutTimer; // timer to generate pulse train
Serial usb(SERIAL_TX, SERIAL_RX); // SERIAL_TX = PA_2, SERIAL_TX = PA_15 - Use for debugging
Serial xbeeSerial(PA_9, PA_10); //
InterruptIn eventIn(PA_12); // capture the pulse input to this pin
DigitalOut statusLed(LED1); // indicate 'running' status
DigitalOut simPulseOut(PB_4);   // Generate pulse train from this pin
DigitalOut sendLed(PB_1);    // Led used to indicate send beep.
volatile int pulseCount = 0; // keep track of number of pulses
volatile int timerTicks = 0; // keep track of number of ticks

// Function prototype/forward declaration for ISR.
void event_irq_measure() {
    pulseCount++;
    //if (pulseCount % 100 == 0) {
       //usb.printf("Detected pulse count: %d\n", pulse_count);
    //}
}

void pulse_out_timer()
{
   simPulseOut = !simPulseOut;
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

    // Form the address fields:
    addr_high[0] = (unsigned char)((XBEE_DESTN_ADDR_64BIT_HIGH >> 24) & 0x000000FF);
    addr_high[1] = (unsigned char)((XBEE_DESTN_ADDR_64BIT_HIGH >> 16) & 0x000000FF);
    addr_high[2] = (unsigned char)((XBEE_DESTN_ADDR_64BIT_HIGH >> 8) & 0x000000FF);
    addr_high[3] = (unsigned char)(XBEE_DESTN_ADDR_64BIT_HIGH & 0x000000FF);

    addr_low[0] = (unsigned char)((XBEE_DESTN_ADDR_64BIT_LOW >> 24) & 0x000000FF);
    addr_low[1] = (unsigned char)((XBEE_DESTN_ADDR_64BIT_LOW >> 16) & 0x000000FF);
    addr_low[2] = (unsigned char)((XBEE_DESTN_ADDR_64BIT_LOW >> 8) & 0x000000FF);
    addr_low[3] = (unsigned char)(XBEE_DESTN_ADDR_64BIT_LOW & 0x000000FF);

    // Form the payload:
    payload[0] = (unsigned char)((numPulses >> 8) & 0x00FF);
    payload[1] = (unsigned char)((numPulses) & 0x00FF);
    payload[2] = 0;
    payload[3] = 0;

    // Form the packet:
    cnt = 0;
    packet[cnt++] = 0x7E;     // start byte
    packet[cnt++] = 0x00;   // length field MSB
    packet[cnt++] = 0x0F;   // length field LSB
    packet[cnt++] = 0x00;   // API identifier
    packet[cnt++] = 0x01;   // Frame ID

    packet[cnt++] = addr_high[0];
    packet[cnt++] = addr_high[1];
    packet[cnt++] = addr_high[2];
    packet[cnt++] = addr_high[3];

    packet[cnt++] = addr_low[0];
    packet[cnt++] = addr_low[1];
    packet[cnt++] = addr_low[2];
    packet[cnt++] = addr_low[3];
    packet[cnt++] = 0x00;             // Options

    packet[cnt++] = payload[0];       // Payload
    packet[cnt++] = payload[1];       // Payload
    packet[cnt++] = payload[2];       // Payload
    packet[cnt++] = payload[3];       // Payload

    checksum = xbee_packet_checksum(packet + 3, cnt-3);
    packet[cnt++] = checksum; // Checksum

    // Send the packet
    for(x=0; x<cnt; x++)
    {
        xbeeSerial.putc(packet[x]);
        usb.printf("%02X ", packet[x]);
    }
    usb.printf("\n\rTotal bytes sent = %d\r\n", cnt);
}

int main() {
    statusTimer.attach(&timer_one_sec, 1.0); // Initialise the status LED timer
    // Tested simPulseOutTimer from 0.01 to 0.001. Able to
    // receive at InterruptIn.
    simPulseOutTimer.attach(&pulse_out_timer, 0.02); // Initialise the pulse output
    usb.printf("RemoteEyes Pulse Capture:\r\n");
    eventIn.rise(&event_irq_measure); // Initialise interrupt in detection on rising edge.
    pulseCount = 0; // Initialise count

    while (1) {
        if(timerTicks >= XBEE_SEND_INTERVAL_SECS)
        {
            sendLed = 1;
            xbee_send(pulseCount);
            usb.printf("Sent pulse count: %d\n\r", pulseCount);
            timerTicks = 0; // reset ticks
            pulseCount = 0; // reset pulse count
            wait(0.02);
            sendLed = 0;
        }
        wait(1);
    }
}
