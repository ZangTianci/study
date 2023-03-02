// gcc uartMain.c uartTool.c -lpthread
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdarg.h>
#include <string.h>
#include <unistd.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <pthread.h>
#include <sys/stat.h>
#include "uartTool.h"


int fd;

void *readSerial(){

    char buffer[32];
    while(1){
        memset(buffer, "\0", sizeof(buffer));
        serialGetStr(fd, buffer);
        printf("get->%s\n", buffer);
    }
}

void *sendSerial(){

    while(1){
        char buffer[32];
        while(1){
            memset(buffer, "\0", sizeof(buffer));
            scanf("%s", buffer);
            serialSendStr(fd, buffer);
        }
    }
}

int main(int argc, char **argv){
   
    char deviceName[32] = {"\0"}; 
    
    pthread_t readt;
    pthread_t sendt;

    if(argc < 2){
        printf("uage:%s /dev/ttyS?\n", argv[0]);
        return -1;
    }
    strcpy(deviceName, argv[1]);

    fd = serialOpen(deviceName, 115200);
    if(fd == -1){
        printf("open %s error\n", deviceName);
    }

    pthread_create(&readt, NULL, readSerial, NULL);
    pthread_create(&sendt, NULL, sendSerial, NULL);

    while(1){
        sleep(10);
    }
    

   return 0;
}

