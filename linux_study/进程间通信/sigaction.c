#include <stdio.h>
#include <signal.h>
#include <unistd.h>

void handler(int signum, siginfo_t *info, void *content)
{
    printf("%d\n", signum);

    if(content != NULL){
        printf("%d\n", info->si_int);
        printf("%d\n", info->si_value.sival_int);
        printf("from %d\n", info->si_pid);
    }
}

int main()
{

    struct sigaction act;
    printf("%d\n", getpid());

    act.sa_sigaction = handler;
    act.sa_flags = SA_SIGINFO;// able to get message

    sigaction(SIGUSR1, &act, NULL);
    while(1);

    return 0;
}