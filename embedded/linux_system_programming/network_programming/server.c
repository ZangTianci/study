#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
// #include <linux/in.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main()
{
    int s_fd;

    struct sockaddr_in s_addr;
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
    int c_fd = accept(s_fd, NULL, NULL);
    // 5.read

    // 6.write

    printf("connect\n");
    while(1);
    return 0;
}
