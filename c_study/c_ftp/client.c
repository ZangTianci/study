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

void handler_server_msg(int fd, struct Msg msg)
{
    int nread;
    struct Msg message;
    int newfilefd;

    nread = read(fd, &message, sizeof(message));
    if(nread == 0){
        printf("server is out ,quit!\n");
        exit(-1);

    }
    else {
        printf("----------\n");
        printf("%s\n", message.data);
        printf("----------\n");

    }

};


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

int cmd_handler(struct Msg msg, int fd)
{

    char *dir = NULL;
    char buf[32];
    int ret;
    int filefd;

    printf("cmd:%s\n", msg.data);
    ret = get_cmd_type(msg.data);

    switch(ret){

        case LS:
        case PWD:
        case CD:
        case GET:
            write(fd, &msg, sizeof(msg));
            break;
        case PUT:
            strcpy(buf, msg.data);
            dir = getDesDir(buf);
            if(access(dir, F_OK) == -1){
                printf("%s not exists\n", dir);
            }
            else{
                filefd = open(dir, O_RDWR);
                read(filefd, msg.secondBuf, sizeof(msg.secondBuf));
                close(filefd);
                write(fd, &msg, sizeof(msg));
            }
            break;
        case LLS:
            system("ls");
            break;
        case LCD:
            dir = getDesDir(msg.data);
            chdir(dir);
            break;
        case QUIT:
            strcpy(msg.data, "quit");
            write(fd, &msg, sizeof(msg));
            close(fd);
            exit(-1);

    }

    return ret;
}

int main(int argc, char **argv)
{
    int s_fd;
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
    // 2.connect
    int con = connect(s_fd, (struct sockaddr *)&s_addr, sizeof(struct sockaddr_in));
    if(con == -1){
        perror("connect");
        exit(-1);
    }
    printf("connect\n");
    int mark = 0;
    // 4.accept
    while(1){
        memset(&c_addr, 0, sizeof(struct sockaddr_in));
        if(mark == 0) printf(">");
        scanf("%s", msg.data);

        int ret = cmd_handler(msg, s_fd);

        if(ret>IFGO){
         
            continue;
        }
        if(ret == -1){
            printf("cmd not\n");
       
            continue;
        }
        handler_server_msg(s_fd, msg);
    }

    return 0;
}
