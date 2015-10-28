#include "msp430g2553.h"
#include "uart.h"

char test_string[8];

int main(void) {
	WDTCTL = WDTPW + WDTHOLD; //Stop WDT
	BCSCTL1 = CALBC1_8MHZ; //Set DCO to 8Mhz
	DCOCTL = CALDCO_8MHZ; //Set DCO to 8Mhz
	P2DIR = 0xFF;                             // All P1.x outputs
  	P2OUT = 0;                                

	uart_init(); //Initialize the UART connection
	int i = 0;
	int j = 0;
	int k = 0;
	__enable_interrupt(); //Interrupts Enabled
	
	while (1) {

		uart_gets(test_string, 8);
		if (test_string == "A")
		{
			//Code here to Set Port 2 to 1
			P2OUT= 0xFF;
		}
		else
		{
			//Code here to Set Port 2 to 0
			P2OUT = 0;
		}

}
