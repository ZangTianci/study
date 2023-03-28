#!/bin/bash
cur_date=`date +%Y-%m-%d`
paths=`df -h|grep /share/external`
index=0
for path in $paths
do    
    index=`expr $index + 1`
    if [ $index -eq 6 ];then
        index=0
        disk_path=$path
    fi
done

rsync -avP /share/Data/0007328458a8/$cur_date /$disk_path/UA/
rsync -avP /share/Data/00073277bb59/$cur_date /$disk_path/UB/
