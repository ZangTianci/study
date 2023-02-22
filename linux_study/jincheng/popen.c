#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


int main(void)
{
    char ret[1024] = {0};
    FILE *f;

    f = popen("ls -l", "r");
    int nread = fread(ret, 1, 1024, f);

    printf("%d, ret=%s\n", nread, ret);
    return 0;
}
