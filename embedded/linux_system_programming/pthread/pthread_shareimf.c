#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

int g_data = 0;

void *func1(void *arg)
{

    printf("%ld thread is create\n", (unsigned long)pthread_self());
    printf("param is %d\n", *((int *)arg));
    while(1){
        printf("t1:%d\n", g_data++);
        sleep(1);
        if(g_data == 3){
            pthread_exit(NULL);
        }
    }

}

void *func2(void *arg)
{

    printf("%ld thread is create\n", (unsigned long)pthread_self());
    printf("param is %d\n", *((int *)arg));
    while(1){
        printf("t2:%d\n", g_data++);
        sleep(1);
    }

}

int main()
{
    int ret1;
    int ret2;
    int param = 100;
    pthread_t t1;
    pthread_t t2;


    ret1 = pthread_create(&t1, NULL, func1, (void *)&param);
    ret2 = pthread_create(&t2, NULL, func2, (void *)&param);
    if(ret1 == 0 && ret2 == 0){
        printf("success\n");
    }
    printf("%ld main is create\n", (unsigned long)pthread_self());
    while(1){
        printf("main:%d\n", g_data++);
        sleep(1);
    }

    
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    
    return 0;
}