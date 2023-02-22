#include <stdio.h>
#include <wiringPi.h>
#include <unistd.h>
#include <sys/time.h>
#include <stdlib.h>

// 调用成功返回0，失败返回-1
// int gettimeofday(struct timeval *tv, struct timezone *tz);
#define Trig 0  //set pin0 as beep control
#define Echo 1

double getDistance()
{
	double dis;

	struct timeval start;
	struct timeval stop;
	
	pinMode(Trig, OUTPUT);
	pinMode(Echo, INPUT);

	digitalWrite(Trig, LOW);
	usleep(5);
	digitalWrite(Trig, HIGH);
	usleep(10);
	digitalWrite(Trig, LOW);

	while(!digitalRead(Echo));
	gettimeofday(&start, NULL);
	while(digitalRead(Echo));
	gettimeofday(&stop, NULL);

	long diffTime = 1000000*(stop.tv_sec-start.tv_sec)+(stop.tv_usec-start.tv_usec);
	dis = (double)diffTime/1000000 * 34000 / 2;

	return dis;

}


int main (void)
{
	double dis;
	if(wiringPiSetup() == -1){
		fprintf(stderr, "%s", "initWringPi error");
		exit(-1);
	}
	while(1){

		dis = getDistance();
		printf("dis=%lf\n", dis);
		usleep(500000);
	}

	return 0;
}
