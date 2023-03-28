#!/bin/bash
cur_date=`date +%Y-%m-%d`
paths=`df -h|grep /media/ztc`
index=0
echo $paths
for path in $paths
do    
    index=`expr $index + 1`
    if [ $index -eq 6 ];then
        index=0
        disk_path=$path
    fi
done
echo $disk_path
