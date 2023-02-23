#include <stdio.h>
#include <pthread.h>

void *func1(void *arg)
{

    printf("%ld thread is create\n", (unsigned long)pthread_self());
    printf("param is %d\n", *((int *)arg));

}

void *func2(void *arg)
{

    printf("%ld thread is create\n", (unsigned long)pthread_self());
    printf("param is %d\n", *((int *)arg));

}

int main()
{
    int ret1;
    int ret2;
    int param = 100;
    pthread_t t1;
    pthread_t t2;

    char *pret = NULL;

    ret1 = pthread_create(&t1, NULL, func1, (void *)&param);
    ret2 = pthread_create(&t2, NULL, func2, (void *)&param);
    if(ret1 == 0 && ret2 == 0){
        printf("success\n");
    }
    printf("%ld main is create\n", (unsigned long)pthread_self());
    
    pthread_join(t1, (void **)&pret);
    pthread_join(t2, (void **)&pret);

    printf("main t1 quit:%s\n", pret);
    
    return 0;
}