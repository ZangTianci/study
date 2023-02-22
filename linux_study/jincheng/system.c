#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
//函数原型：int execl(const char *path, const char *arg, ...);

int main(void)
{
    printf("before system\n");
    if(system("ls -l") == -1)
    {
        printf("system failed!\n");     
        perror("why"); 
    }
    printf("after system\n");
    return 0;
}
