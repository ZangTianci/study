#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>

int main(){

    char *str = "message from fifo";

    int fd = open("./file", O_WRONLY);
    if(fd == -1){
        printf("file does not exist");
    }
    else{
        write(fd, str, strlen(str));
        close(fd);
        printf("write success\n");
    }
    

    


    return 0;
}
