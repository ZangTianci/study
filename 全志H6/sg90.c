#include <stdio.h>
#include <wiringPi.h>
#include <unistd.h>
#include <sys/time.h>
#include <stdlib.h>
#include <signal.h>

#define SG90Pin 5

int angle = 2;
static int i = 0;

void signal_handler(int signum)
{
	i++;
	if(i <= angle){
		digitalWrite(SG90Pin, HIGH);
	}
	else{
		digitalWrite(SG90Pin, LOW);
	}
	if(i == 40){
		i = 0;
	}
}

int main (void)
{
	struct itimerval itv;
	angle = 0;
	wiringPiSetup();
	pinMode(SG90Pin, OUTPUT) ;

	//设定开始生效，启动定时器的时间
	itv.it_value.tv_sec = 1;
	itv.it_value.tv_usec = 0;
	
	//设定定时时间
	itv.it_interval.tv_sec = 0;
	itv.it_interval.tv_usec = 500;
	//设定定时方式
	if(setitimer(ITIMER_REAL, &itv, NULL) == -1){
		perror("error");
		exit(-1);
	}
	//信号处理
	signal(SIGALRM,signal_handler);

	while(1){
		printf("input angle:1-0, 2-45, 3-90, 4-135");
		scanf("%d", &angle);
	}

	return 0;
}
