#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

int g_data = 0;

pthread_mutex_t mutex;

void *func1(void *arg)
{
    
    printf("%ld thread1 is create\n", (unsigned long)pthread_self());
    printf("param is %d\n", *((int *)arg));
    pthread_mutex_lock(&mutex);
    while(1){
        
        if(g_data == 3){
            pthread_mutex_unlock(&mutex);
            printf("**********t1quit************");
            pthread_exit(NULL); 
        }
    }
}

void *func2(void *arg)
{
    
    printf("%ld thread2 is create\n", (unsigned long)pthread_self());
    printf("param is %d\n", *((int *)arg));
    while(1){
        pthread_mutex_lock(&mutex);
        printf("t2:%d\n", g_data++);
        pthread_mutex_unlock(&mutex);
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

    pthread_mutex_init(&mutex, NULL);

    ret1 = pthread_create(&t1, NULL, func1, (void *)&param);
    ret2 = pthread_create(&t2, NULL, func2, (void *)&param);
    if(ret1 == 0 && ret2 == 0){
        printf("success\n");
    }
    printf("%ld main is create\n", (unsigned long)pthread_self());
    while(1){
        printf("main:%d\n", g_data);
        sleep(1);
    }

    
    
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    pthread_mutex_destroy(&mutex);

    
    return 0;
}