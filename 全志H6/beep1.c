#include <stdio.h>
#include <wiringPi.h>
#include <unistd.h>


#define BEEP 0  //set pin0 as beep control

int main (void)
{
	wiringPiSetup () ;// initialize wiringPi

	pinMode (BEEP, OUTPUT) ;// set io port input or output	

	digitalWrite (BEEP, LOW);
	sleep(1);
	digitalWrite (BEEP, HIGH);

	return 0;
}
