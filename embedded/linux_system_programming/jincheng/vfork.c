#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>


int main(int argc, char **argv)
{
    pid_t pid;
    pid_t pid2;
    int data = 10;
    int cnt = 0;
    
    while(1){
        printf("please input a value\n");
        scanf("%d", &data);
        if(data == 1){
            pid = fork();
            if(pid > 0){
                printf("%d\n", getpid());
                printf("cnt=%d", cnt);
            }
            else if(pid == 0){
                while(1){
                    printf("%d\n", getpid());
                    sleep(3);
                    cnt++;
                    if(cnt == 3){
                        exit(0);
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