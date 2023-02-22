#include <stdio.h>


int main(int argc, char **argv)
{
    
    FILE *fp;
    char *str = "zangtianci shuai de";

    fp = fopen("./chen.txt", w+);

    fwrite(str, sizeof(char), strlen(str), fp);

    fread(readBuf, szieof(char), );





    return 0;
}