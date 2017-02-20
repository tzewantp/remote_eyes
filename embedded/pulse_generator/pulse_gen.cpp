/* Simple program to generate pulses from PB_1 of STM32Nucleo F042K6 and receive at PA_12 */

#include "mbed.h"

Ticker pulse_timer; // timer to generate the output pulse train from PA_12
Ticker status_timer; // 1 sec timer for the LED to indicate 'running' status
Serial usb(SERIAL_TX, SERIAL_RX); // SERIAL_TX = PA_2, SERIAL_TX = PA_15 - Use for debugging
InterruptIn event_in(PA_12); // capture the pulse input to this pin
DigitalOut pulse_out(PB_1); // generate the pulse train out from this pin
DigitalOut status_led(LED1); // indicate 'running' status
volatile int pulse_count = 0; // keep track of number of pulses

// Function prototype/forward declaration for ISR.
void event_irq_measure() {
    pulse_count++;
    if (pulse_count % 100 == 0) {
       usb.printf("Detected pulse count: %d\n", pulse_count);
    }
}

// Timer event to generate the pulse train
void pulse_out_timer() {
   pulse_out = !pulse_out;
}

// Timer event to toggle the status LED
void timer_one_sec() {
   status_led = !status_led;
}

int main() {
    status_timer.attach(&timer_one_sec, 1.0); // Initialise the status LED timer
    pulse_timer.attach(&pulse_out_timer, 0.01); // Initialise the pulse output timer
    usb.printf("Pulse counting program:\n");
    event_in.rise(&event_irq_measure); // Initialise interrupt in detection on rising edge.
    pulse_count = 0; // Initialise count

    while (1) {

    }
}

