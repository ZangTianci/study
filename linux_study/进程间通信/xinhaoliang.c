#include <stdio.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

union semun{
    int val;                   //SETVAL的值
    struct semid_ds *buf;      //IPC_STAT，IPC_SET的缓冲区 
    unsigned short *array;      //GETALL，SETALL的数组
    struct seminfo *__buf;       //IPC_INFO的缓冲区（特定于Linux）
};

void pGetKey(int id){

    struct sembuf set;
    set.sem_num = 0;
    set.sem_op = -1;
    set.sem_flg = SEM_UNDO;
    semop(id, &set, 1);
    printf("getkey\n");

}

void vGetBackKey(int id){

    struct sembuf set;
    set.sem_num = 0;
    set.sem_op = 1;
    set.sem_flg = SEM_UNDO;
    semop(id, &set, 1);
    printf("getbackkey\n");

}


int main(int argc, char const *argv[]){

    key_t key;
    int semid;
    key = ftok(".", 2);

    semid = semget(key, 1, IPC_CREAT|0666);// 获取、创建信号量

    union semun initsem;
    initsem.val = 0;
    // 操作第0个信号量
    semctl(semid, 0, SETVAL, initsem);

    int pid = fork();
    if(pid>0){
        // 拿锁
        pGetKey(semid);
        printf("father\n");
        vGetBackKey(semid);
    }
    else if(pid == 0){
        printf("child\n");
        vGetBackKey(semid);
    }
    else{
        printf("failed\n");
    }

    return 0;
}