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
#include <stdlib.h>


int main(){

    int shmid;
    char *shmaddr;
    key_t key;
    key = ftok(".", 1);

    shmid = shmget(key, 1024*4, IPC_CREAT);
    if(shmid == -1){
        printf("failed\n");
        exit(-1);
    }
    shmaddr = shmat(shmid, 0, 0);

    printf("shmat ok\n");
    printf("%s\n", shmaddr);


    shmdt(shmaddr);
    shmctl(key, IPC_RMID, 0);

    printf("exit\n");

    return 0;


    
}
