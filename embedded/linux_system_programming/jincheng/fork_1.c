#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>


int main(int argc, char **argv)
{
    pid_t pid;
    pid_t pid2;
    int data = 10;
    
    while(1){
        printf("please input a value\n");
        scanf("%d", &data);
        if(data == 1){
            pid = fork();
            if(pid > 0){
                printf("%d\n", getpid());
            }
            else if(pid == 0){
                while(1){
                    printf("%d\n", getpid());
                    sleep(5);
                }
            }
        }
        else{
            printf("nothing\n");
        }
    }



    return 0;

}