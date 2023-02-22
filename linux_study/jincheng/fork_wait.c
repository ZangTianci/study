#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>


int main(int argc, char **argv)
{
    pid_t pid;
    pid_t pid2;
    int data = 10;
    int cnt = 0;
    int wstatus = 10;
    
    while(1){
        printf("please input a value\n");
        scanf("%d", &data);
        if(data == 1){
            pid = fork();
            if(pid > 0){
                wait(&wstatus);
                printf("%d\n", WEXITSTATUS(wstatus));
                while(1){
                    sleep(1);
                    printf("%d\n", getpid());
                    printf("cnt=%d\n", cnt);
                }
            }
            else if(pid == 0){
                while(1){
                    printf("%d\n", getpid());
                    sleep(1);
                    cnt++;
                    if(cnt == 3){
                        exit(3);
                    }
                }
            }
        }
        else{
            printf("nothing\n");
        }
    }



    return 0;

}