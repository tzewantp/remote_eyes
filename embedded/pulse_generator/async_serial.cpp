#include "mbed.h"

/*------------ Constant definitions --------------*/
#define TX_PIN          USBTX
#define RX_PIN          USBRX
#define BAUDRATE        115200
#define LED_PIN         LED0
#define TOGGLE_RATE     (0.5f)
#define BUFF_LENGTH     5

/*-------- Check if platform compatible ----------*/
#if DEVICE_SERIAL_ASYNCH
Serial pc_connection(TX_PIN, RX_PIN);
#else
#error "Platform not compatible with Low Power APIs for Serial"
#endif

/*------------------ Variables -------------------*/
Ticker              blinker;
bool                blinking = false;
event_callback_t    serial_event;
DigitalOut          LED(LED1);
uint8_t             rx_buf[BUFF_LENGTH + 1];

/*------------------ Callbacks -------------------*/
void blink(void) {
    LED = !LED;
}

/**
* This is a callback! Do not call frequency-dependent operations here.
*
* For a more thorough explanation, go here: 
* https://developer.mbed.org/teams/SiliconLabs/wiki/Using-the-improved-mbed-sleep-API#mixing-sleep-with-synchronous-code
**/
void serial_callback_function(int events) {
    /* Something triggered the callback, either buffer is full or 'S' is received */
    unsigned char i;
    if(events & SERIAL_EVENT_RX_CHARACTER_MATCH) {
        // Received 'S', check for buffer length
        for(i = 0; i < BUFF_LENGTH; i++) {
            // Found the length!
            if(rx_buf[i] == 'S') break;
        }
        
        // Toggle blinking
        if(blinking) {
            blinker.detach();
            blinking = false;
        } 
        else {
            blinker.attach(blink, TOGGLE_RATE);
            blinking = true;
        }
    } 
    else if (events & SERIAL_EVENT_RX_COMPLETE) {
        i = BUFF_LENGTH - 1;
    } 
    else {
        rx_buf[0] = 'E';
        rx_buf[1] = 'R';
        rx_buf[2] = 'R';
        rx_buf[3] = '!';
        rx_buf[4] = 0;
        i = 3;
    }
    
    // Echo string, no callback
    pc_connection.write(rx_buf, i+1, 0, 0);
    
    // Reset serial reception
    pc_connection.read(rx_buf, BUFF_LENGTH, serial_event, SERIAL_EVENT_RX_ALL, 'S');
}

/*-------------------- Main ----------------------*/
int main() {

    /* Setup the event for handling asynchronous serial receiving */
    serial_event.attach(serial_callback_function);
    
    /* Setup serial connection */
    pc_connection.baud(BAUDRATE);
        
    pc_connection.printf("\n=====================================================\n");
    pc_connection.printf("\n\nmbed STM32F401RE Nucleo : My Simple Pulse Generator\n\n");
    pc_connection.printf("\n=====================================================\n");
    pc_connection.printf("\nPress:\n");
    pc_connection.printf("\n'S' : To toggle blinking.\n\n");
    pc_connection.read(rx_buf, BUFF_LENGTH, serial_event, SERIAL_EVENT_RX_ALL, 'S');
    
    /* Let the callbacks take care of everything */
    while(1) 
    {
        sleep();
    }
}
