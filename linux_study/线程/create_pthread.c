#include <stdio.h>
#include <pthread.h>


// int pthread_create(pthread_t *restrict tidp, const pthread_attr_t *restrict attr, void *(*start_rtn)(void *), void *restrict arg);

void *func1(void *arg)
{
    printf("%ld thread is create\n", (unsigned long)pthread_self());
    printf("param is %d\n", *((int *)arg));
}

int main(int argc, int **argv[])
{
    int ret;
    int param = 100;
    pthread_t t1;

    ret = pthread_create(&t1, NULL, func1, (void *)&param);
    if(ret == 0){
        printf("success\n");
    }
    printf("%ld main is create\n", (unsigned long)pthread_self());
    pthread_join(t1, NULL);
    
    return 0;
}