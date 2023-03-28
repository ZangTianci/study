#!/bin/bash
des_date=`date +%Y-%m-%d`
cur_time=`date +%H`
# des_date=$1
path10="/home/ztc/Nas/Log/$des_date"
path1="$path10/$cur_time"
path20="/media/ztc/Data/work/LOG/$des_date"
path2="$path20/$cur_time"
# des_time=$1 # 0：0-11点，1：12-23点，2：0-23点
des_time=2

mkdir $path10
mkdir $path1
mkdir $path1/chhs
mkdir $path1/chhs/LA_19
mkdir $path1/chhs/LB_17
mkdir $path1/chhs/UA_21
mkdir $path1/chhs/UB_28
mkdir $path1/mtc
mkdir $path1/mtc/LA_48
mkdir $path1/mtc/LB_49
mkdir $path1/mtc/UA_50
mkdir $path1/mtc/UB_47
mkdir $path1/kone
mkdir $path1/kone/LA_51
mkdir $path1/kone/LB_55

mkdir $path20
mkdir $path2
mkdir $path2/chhs
mkdir $path2/chhs/LA_19
mkdir $path2/chhs/LB_17
mkdir $path2/chhs/UA_21
mkdir $path2/chhs/UB_28
mkdir $path2/mtc
mkdir $path2/mtc/LA_48
mkdir $path2/mtc/LB_49
mkdir $path2/mtc/UA_50
mkdir $path2/mtc/UB_47
mkdir $path2/kone
mkdir $path2/kone/LA_51
mkdir $path2/kone/LB_55

echo "child_hosp_upper_vpm_21"
ssh child_hosp_upper_vpm_21 "cd /home/magicdepth/ztc/;bash getlog.sh"
scp child_hosp_upper_vpm_21:/home/magicdepth/ztc/dpmlog.zip $path2/chhs/UA_21
scp child_hosp_upper_vpm_21:/home/magicdepth/ztc/vpmlog.zip $path2/chhs/UA_21
scp $path2/chhs/UA_21/dpmlog.zip $path1/chhs/UA_21
scp $path2/chhs/UA_21/vpmlog.zip $path1/chhs/UA_21
unzip -d $path2/chhs/UA_21 $path2/chhs/UA_21/dpmlog.zip
unzip -d $path2/chhs/UA_21 $path2/chhs/UA_21/vpmlog.zip
rm $path2/chhs/UA_21/dpmlog.zip
rm $path2/chhs/UA_21/vpmlog.zip
bash /home/ztc/code/getlogDaily/loginmd.sh $path2/chhs/UA_21 $des_date 2 UA_21 $cur_time chhs