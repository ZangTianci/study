#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
// #include <linux/in.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>

int main()
{
    int c_fd;
    char readBuf[128];
    char *msg = "i got your message";

    struct sockaddr_in c_addr;

    // 用memset做数据清空

    memset(c_addr, 0, sizeof(struct sockaddr_in));

    c_addr.sin_family = AF_INET;
    c_addr.sin_port = htons(8989);// 5000-9000
    inet_aton("127.0.0.1", &s_addr.sin_addr);

    // 1.socket
    c_fd = socket(AF_INET, SOCK_STREAM, 0);
    if(c_fd == -1){
        perror("socket");
        exit(-1);
    }
    // 2.connect
    int con = connect(c_fd, (struct sockaddr *)&c_addr, sizeof(struct sockaddr));
    if(con == -1){
        perror("connect");
        exit(-1);
    }
    printf("get connect: %s\n", *p);
    
    // 3.send
    write(c_fd, msg, strlen(msg));
    
    // 4.read
    int nread = read(c_fd, readBuf, 128);
    if(nread == -1){
        perror("read");
    }
    else{
        printf("get message %d, %s\n", nread, read);
    }


    return 0;
}
