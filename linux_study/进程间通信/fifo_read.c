#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

#include <sys/stat.h>
#include <errno.h>
#include <fcntl.h>


int main(){


    char buff[30] = {0};

    if((mkfifo("./file", 0666) == -1) && errno != EEXIST){
        printf("mkfifo failed\n");
        perror("why");
    }

    int fd = open("./file", O_RDONLY);
    
    printf("open success\n");

    int nread = read(fd, buff, 30);
    close(fd);
    printf("read %d from fifo content=%s", nread, buff);

    return 0;
}
