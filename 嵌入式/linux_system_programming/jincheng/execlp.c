#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
//函数原型：int execl(const char *path, const char *arg, ...);

int main(void)
{
    printf("before execl\n");
    if(execlp("ls","-l",NULL) == -1)
    {
        printf("execlp failed!\n");     
        perror("why"); 
    }
    printf("after execl\n");
    return 0;
}
