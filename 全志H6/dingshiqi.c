#include <stdio.h>
#include <wiringPi.h>
#include <unistd.h>
#include <sys/time.h>
#include <stdlib.h>
#include <signal.h>

static int i;

void signal_handler(int signum)
{
	i++;
	if(i == 2000){
		printf("hello\n");
		i = 0;
	}
}

int main (void)
{
	struct itimerval itv;

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

	while(1);

	return 0;
}
