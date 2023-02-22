#include <stdio.h>
#include <signal.h>


void handler(int signum)
{
    printf("get signum = %d\n", signum);
    printf("never quit\n");
}

int main()
{
    // ctrl+c
    signal(SIGINT, handler);
    while(1);

    return 0;
}