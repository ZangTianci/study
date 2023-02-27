#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>


int main(int argc, char **argv)
{
    pid_t pid;
    pid_t pid2;
    int data = 10;
    
    pid = getpid();

    fork();
    pid2 = getpid();
    printf("my %d, cur %d\n", pid, pid2);
    printf("data = %d\n", data);

    return 0;

}