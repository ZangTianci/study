#include <stdio.h>
#include <unistd.h>

int main(){

    int fd[2];

    int pid;

    if(pipe(fd) == -1){
        printf("create pipe failed\n");
    }

    pid = fork();
    if(pid<0){
        printf("create child failed\n");
    }
    else if(pid > 0){
        printf("this is father\n");
    }
    else{
        printf("this is child\n");
    }

    return 0;
}
