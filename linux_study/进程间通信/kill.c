#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/stat.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <stdlib.h>
#include <signal.h>


int main(int argc, char **argv)
{
    int signum;
    int pid;

    signum = atoi(argv[1]);
    pid = atoi(argv[2]);

    printf("%d\n%d\n", signum, pid);
    // 信号发送
    kill(pid, signum);

    return 0;
}