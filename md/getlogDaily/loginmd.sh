#!/bin/bash

path=$1
des_date=$2 # 2022-06-05
des_time=$3 # 0：0-11点，1：12-23点，2：0-23点
loca=$4
curtime=$5
where=$6
cur_date=`date +%Y_%m_%d_%H`

# 生成需要拉取的时段
if [[ "0" == $des_time ]]; then
    des_time_start=0
    des_time_end=11
elif [[ "1" == $des_time ]]; then
    des_time_start=7
    des_time_end=19
else
    des_time_start=0
    des_time_end=23
fi

# grep -E "2022-06-05 03|2022-06-05 04" 
for ((i = $des_time_start; i <= $des_time_end; ++i)); do
    hour=`printf "%02d\n" $i`
    cond_time=$cond_time"$des_date $hour"
    if [ $i -ne $des_time_end ]; then
        cond_time=$cond_time"|"
    fi
done


MAX=12
for ((i = 1; i <= $MAX; ++i)); do
    code=E`printf "1%03d\n" $i`
    # code=E`printf "%04d\n" $i`
    count1=`cat $path/opt/log/LOG_ODM_System_1.txt | grep "App error code: $code" |grep -E "\"$des_date\"" | wc -l`
    count2=`cat $path/opt/log/LOG_ODM_System_2.txt | grep "App error code: $code" |grep -E "\"$des_date\"" | wc -l`
    count=`expr $count1 + $count2`
    echo $count>>/media/ztc/Data/work/LOG/$des_date/$curtime/$where/$loca"vpmlog".txt
done
MIN=9
for ((i = 1; i <= $MIN; ++i)); do
    code10=E`printf "2%03d\n" $i`
    count110=`cat $path/home/magicdepth/ztc/dpmlog/LOG_ODM_System_1.txt | grep "App error code: $code10" |grep -E "\"$des_date\"" | wc -l`
    count210=`cat $path/home/magicdepth/ztc/dpmlog/LOG_ODM_System_2.txt | grep "App error code: $code10" |grep -E "\"$des_date\"" |  wc -l`
    count10=`expr $count110 + $count210`
    echo $count10>>/media/ztc/Data/work/LOG/$des_date/$curtime/$where/$loca"dpmlog".txt
done

MMM=2
for ((i = 1; i <= $MMM; ++i)); do
    code100="ATCF$i"
    count1100=`cat $path/opt/log/LOG_ODM_System_1.txt | grep "$code100" |grep -E "\"$des_date\"" | wc -l`
    count2100=`cat $path/opt/log/LOG_ODM_System_2.txt | grep "$code100" |grep -E "\"$des_date\"" | wc -l`
    count100=`expr $count1100 + $count2100`
    echo $count100>>/media/ztc/Data/work/LOG/$des_date/$curtime/$where/$loca"atcf".txt
done