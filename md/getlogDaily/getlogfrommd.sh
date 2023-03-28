#!/bin/bash
cur_datetime=`date +%Y_%m_%d_%H`
cur_date=`date +%Y-%m-%d`
cur_time=`date +%H`

path10="/home/ztc/Nas/Log/$cur_date"
path1="$path10/$cur_time"
path20="/media/ztc/Data/work/LOG/$cur_date"
path2="$path20/$cur_time"
# des_time=$1 # 0：0-11点，1：12-23点，2：0-23点
des_time=2
# vpmid=$1

for vpmid in 22 24 30
do 
    mkdir $path10
    mkdir $path1
    mkdir $path1/MD
    mkdir $path1/MD/VPM$vpmid
    mkdir $path20
    mkdir $path2
    mkdir $path2/MD
    mkdir $path2/MD/VPM$vpmid

    echo "VPM$vpmid"
    ssh magicdepth@192.168.1.$vpmid "cd /home/magicdepth/ztc/;bash getlog.sh"
    scp magicdepth@192.168.1.$vpmid:/home/magicdepth/ztc/dpmlog.zip $path2/MD/VPM$vpmid
    scp magicdepth@192.168.1.$vpmid:/home/magicdepth/ztc/vpmlog.zip $path2/MD/VPM$vpmid
    scp $path2/MD/VPM$vpmid/dpmlog.zip $path1/MD/VPM$vpmid
    scp $path2/MD/VPM$vpmid/vpmlog.zip $path1/MD/VPM$vpmid
    unzip -d $path2/MD/VPM$vpmid $path2/MD/VPM$vpmid/dpmlog.zip
    unzip -d $path2/MD/VPM$vpmid $path2/MD/VPM$vpmid/vpmlog.zip
    rm $path2/MD/VPM$vpmid/dpmlog.zip
    rm $path2/MD/VPM$vpmid/vpmlog.zip
    bash /home/ztc/code/getlogDaily/loginmd.sh $path2/MD/VPM$vpmid $cur_date $des_time VPM$vpmid $cur_time
done


