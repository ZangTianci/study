#include "twoSum.h"

void twoSum(int* nums, int numsSize, int target, int* returnSize){
    int i, j;
    int sum;

    for(i=0; i<numsSize; i++){
        for(j=i+1; j<numsSize; j++){
            sum = nums[i] + nums[j];
            printf("%d, %d, %d\n",i,j,sum);
            if(sum == target){
                returnSize[0] = i;
                returnSize[1] = j;
            }
        }
    }
}

void twoSumTest()
{
    int nums[4] = {2,7,11,15};
    // int num[3] = {3,2,4};6 [1,2]
    // int num[2] = {3,3};6 [0,1]
    
    int returnSize[2] = {0};
    twoSum(nums, 4, 9, returnSize);
    printf("%d, %d\n", returnSize[0], returnSize[1]);
}