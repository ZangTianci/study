#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
// #include <linux/in.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    int c_fd;
    int s_fd;
    int nread;
    char readBuf[128];
    char msg[128] = {0};

    struct sockaddr_in c_addr;
    struct sockaddr_in s_addr;

    if(argc != 3){
        printf("plz input 3 arg");
        exit(-1);
    }

    // 用memset做数据清空
    memset(&s_addr, 0, sizeof(struct sockaddr_in));
    memset(&c_addr, 0, sizeof(struct sockaddr_in));

    s_addr.sin_family = AF_INET;
    s_addr.sin_port = htons(atoi(argv[2]));// 5000-9000
    inet_aton(argv[1], &s_addr.sin_addr);

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
    while(1){
        c_fd = accept(s_fd, (struct sockaddr *)&c_addr, &c_len);
        if(c_fd == -1){
            perror("accept");
            exit(-1);
        }
        printf("get connect: %s\n", inet_ntoa(c_addr.sin_addr));
        if(fork() == 0){
            
            if(fork() == 0){
                while(1){
                    memset(msg, 0, sizeof(msg));
                    printf("plz input");
                    scanf("%s", msg);
                    write(c_fd, msg, strlen(msg));
                }
            }
            while(1){
                memset(readBuf, 0, sizeof(readBuf));
                // 5.read
                nread = read(c_fd, readBuf, 128);
                if(nread == -1){
                    perror("read");
                }
                else{
                    printf("get message %d, %s\n", nread, readBuf);
                    // 6.write
                
                }
            }
            
            break;
        }
        
    }

    return 0;
}
