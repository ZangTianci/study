#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/stat.h>
// #include <linux/in.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include </home/ztc/code/study/c_study/c_ftp/config.h>

char *getDesDir(char *cmsg)
{
    char *p;
    p = strtok(cmsg, " ");
    p = strtok(NULL, " ");
    return p;

}

int get_cmd_type(char *cmd)
{
    if(!strcmp("ls", cmd))   
        return LS;
    if(strstr("get", cmd) != NULL)   
        return GET;
    if(!strcmp("pwd", cmd))   
        return PWD;
    if(!strcmp("ifgo", cmd))   
        return IFGO;
    if(!strcmp("lcd", cmd))   
        return LCD;
    if(!strcmp("lls", cmd))   
        return LLS;
    if(strstr("cd", cmd) != NULL)   
        return CD;
    if(strstr("put", cmd) != NULL)   
        return PUT;
    if(!strcmp("quit", cmd))   
        return QUIT;
    if(!strcmp("dofile", cmd))   
        return DOFILE;

}

void msg_handler(struct Msg msg, int fd)
{
    char dataBuf[1024] = {0};
    char *file = NULL;
    int fdfile;
    

    printf("cmd:%s\n", msg.data);
    int ret = get_cmd_type(msg.data);

    switch(ret){

        case LS:
        case PWD:{
            FILE *r = popen(msg.data, "r");
            fread(msg.data, sizeof(msg.data), 1, r);
            write(fd, &msg, sizeof(msg));
            break;}
        case CD:
            {char *dir = getDesDir(msg.data);
            printf("dir:%s\n", dir);
            chdir(dir);
            break;}
        case GET:
            file = getDesDir(msg.data);
            if(access(file, F_OK) == -1){
                strcpy(msg.data, "no this file");
                write(fd, &msg, sizeof(msg));
            }
            else{
                fdfile = open(file , O_RDWR);
                read(fdfile, dataBuf, sizeof(dataBuf));
                close(fdfile);

                strcpy(msg.data, dataBuf);
                write(fd, &msg, sizeof(msg));
            }
            break;
        case PUT:
            file = getDesDir(msg.data);
            fdfile = open(file, O_RDWR|O_CREAT, 0666);
            write(fdfile, msg.secondBuf, strlen(msg.secondBuf));
            close(fdfile);
            break;
        case QUIT:
            printf("client quit\n");
            exit(-1);

    }
}

int main(int argc, char **argv)
{
    int s_fd;
    int c_fd;
    int nread;
    struct Msg msg;
    
    struct sockaddr_in s_addr;
    struct sockaddr_in c_addr;
    memset(&s_addr, 0, sizeof(struct sockaddr_in));
    s_addr.sin_family = AF_INET;
    s_addr.sin_port = htons(atoi(argv[2]));
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
    int clen = sizeof(struct sockaddr_in);
    // 4.accept
    while(1){
        memset(&c_addr, 0, sizeof(struct sockaddr_in));
        c_fd = accept(s_fd, (struct sockaddr *)&c_addr, &clen);
        if(c_fd == -1){
            perror("accept");
            exit(-1);
        }
        printf("get connect:%s\n", inet_ntoa(c_addr.sin_addr));
        if(fork() == 1){
            while(1){
                memset(msg.data, 0, sizeof(struct sockaddr_in));
                nread = read(c_fd, &msg, sizeof(msg));
                if(nread == 0){
                    printf("client out\n");
                    break;
                }
                else if(nread > 0){
                    msg_handler(msg, c_fd);
                }

            }
        }
    }

    return 0;
}
