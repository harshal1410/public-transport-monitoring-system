#include "msp430g2553.h"
#include "uart.h"

char test_string[8];

int main(void) {
	WDTCTL = WDTPW + WDTHOLD; //Stop WDT
	BCSCTL1 = CALBC1_8MHZ; //Set DCO to 8Mhz
	DCOCTL = CALDCO_8MHZ; //Set DCO to 8Mhz

	uart_init(); //Initialize the UART connection
	int i = 0;
	int j = 0;
	int k = 0;
	__enable_interrupt(); //Interrupts Enabled

	while (1) {

		uart_puts((char *) "BUS-STAND10001\n");

		for (i = 0; i < 255; i++) {
			for (j = 0; j < 255; j++) {
				for (k = 0; k < 255; k++) {
				}
			}
		}
	}

}
