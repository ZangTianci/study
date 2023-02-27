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
    int s_fd;
    char readBuf[128];
    char *msg = "i got your message";

    struct sockaddr_in c_addr;
    struct sockaddr_in s_addr;
    // 用memset做数据清空
    memset(s_addr, 0, sizeof(struct sockaddr_in));
    memset(c_addr, 0, sizeof(struct sockaddr_in));

    s_addr.sin_family = AF_INET;
    s_addr.sin_port = htons(8989);// 5000-9000
    inet_aton("127.0.0.1", &s_addr.sin_addr);

    // 1.socket
    s_fd = socket(AF_INET, SOCK_STREAM, 0);
    if(s_fd == -1){
        perror("socket");
        exit(-1);
    }
    // 2.bind
    bind(s_fd, (struct sockaddr *)&s_addr, sizeof(struct sockaddr_in));
    // 3.listen
    listen(s_fd, 10);
    // 4.accept
    int c_len = sizeof(struct sockaddr_in);
    int c_fd = accept(s_fd, (struct sockaddr *)&c_addr, &c_len);
    if(s_fd == -1){
        perror("accept");
        exit(-1);
    }
    char *p = inet_ntoa(&c_addr.sin_addr);
    printf("get connect: %s\n", *p);
    // 5.read
    int nread = read(c_fd, readBuf, 128);
    if(nread == -1){
        perror("read");
    }
    else{
        printf("get message %d, %s\n", nread, read);
    }
    // 6.write
    write(c_fd, msg, strlen(msg));


    return 0;
}
