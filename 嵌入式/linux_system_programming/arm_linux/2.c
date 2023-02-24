#include <stdio.h>

int main()
{
    int a =1;
    int *p;
    p = &a;
    int b = *p;
    printf("%d", *p);
    printf("%d", b);
}