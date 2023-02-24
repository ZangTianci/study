#include <stdio.h>

int p1;
int p2;




float lianfen(float sum, int a){
    int i;
    if(sum == 0){
        sum = a;
        p1 = a;
        p2 = 1;
    }
    else{
        sum = a + 1 / sum;
        i = p1;
        p1 = a * p1 + p2;
        p2 = i;
    }
    
    printf("%d\n", a);
    printf("after %f\n", sum);
    
    return sum;
}

void test(int *cont, int size){
    float sum = 0;
    int i;
    
    for(i = size - 1; i>=0; i--){
        sum = lianfen(sum, cont[i]);
        printf("%f\n", sum);
    }
    // for(i=9; i>0; i--){
    //     if(p1%i == 0){
    //         if(p1/i >= 1){
    //             if(p2/i >= 1){
    //                 p1 = p1/i;
    //                 p2 = p2/i;
    //             }
    //         }
    //     }
    // }
    printf("%d\n", p1);
    printf("%d\n", p2);
}

int main()
{
    int cont[5] = {9, 5, 7, 1, 3};
    int size = sizeof(cont)/sizeof(int);
    printf("size_cont = %ld, size_int = %ld, size = %d\n", sizeof(cont), sizeof(int), size);
    test(cont, size);

    return 0;
}