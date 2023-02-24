#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>


int main(int argc, char **argv)
{
    int signum;
    int pid;

    signum = atoi(argv[1]);
    pid = atoi(argv[2]);

    union sigval value;
    value.sival_int = 100;

    sigqueue(pid, signum, value);

    while(1);

    return 0;
}