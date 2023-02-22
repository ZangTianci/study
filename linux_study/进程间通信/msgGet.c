#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/stat.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>


struct msgbuf {
    long mtype;       /* message type, must be > 0 */
    char mtext[128];    /* message data */
};

int main(){

    struct msgbuf readbuf;

    int msgid = msgget(0x1234, IPC_CREAT|0777);
    if(msgid == -1){
        printf("get que failed");
    }
    msgrcv(msgid, &readbuf, sizeof(readbuf.mtext), 888, 0);
    printf("%s\n", readbuf.mtext);

    return 0;
}
