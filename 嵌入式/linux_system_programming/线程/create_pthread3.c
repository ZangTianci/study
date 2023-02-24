#include <stdio.h>
#include <pthread.h>


// int pthread_create(pthread_t *restrict tidp, const pthread_attr_t *restrict attr, void *(*start_rtn)(void *), void *restrict arg);

void *func1(void *arg)
{
    static char *p = "t1 is exit";

    printf("%ld thread is create\n", (unsigned long)pthread_self());
    printf("param is %d\n", *((int *)arg));

    pthread_exit((void *)p);
}

int main()
{
    int ret;
    int param = 100;
    pthread_t t1;

    char *pret = NULL;

    ret = pthread_create(&t1, NULL, func1, (void *)&param);
    if(ret == 0){
        printf("success\n");
    }
    printf("%ld main is create\n", (unsigned long)pthread_self());
    pthread_join(t1, (void **)&pret);

    printf("main t1 quit:%s\n", pret);
    
    return 0;
}