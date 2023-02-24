#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char **argv)
{
    
    int fdSrc;

    if(argc != 2){
        printf("error\n");
        exit(-1);
    }
    fdSrc = open(argv[1], O_RDWR);
    int size = lseek(fdSrc, 0, SEEK_END);
    lseek(fdSrc, 0, SEEK_SET);
    char *readBuf = (char *)malloc(sizeof(char)*size+8);
    int n_read = read(fdSrc, readBuf, size);
    char *p = strstr(readBuf, "LONG=");
    if(p==NULL){
        printf("erro\n");
        exit(-1);
    }
    p = p+strlen("LONG=");
    *p = '5';
    int n_write = write(fdSrc, readBuf, strlen(readBuf));
    close(fdSrc);
    return 0;
}