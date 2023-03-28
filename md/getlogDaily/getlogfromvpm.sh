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

# echo "child_hosp_upper_vpm_21"
# ssh child_hosp_upper_vpm_21 "cd /home/magicdepth/ztc/;bash getlog.sh"
# scp child_hosp_upper_vpm_21:/home/magicdepth/ztc/dpmlog.zip $path2/chhs/UA_21
# scp child_hosp_upper_vpm_21:/home/magicdepth/ztc/vpmlog.zip $path2/chhs/UA_21
# scp $path2/chhs/UA_21/dpmlog.zip $path1/chhs/UA_21
# scp $path2/chhs/UA_21/vpmlog.zip $path1/chhs/UA_21
# unzip -d $path2/chhs/UA_21 $path2/chhs/UA_21/dpmlog.zip
# unzip -d $path2/chhs/UA_21 $path2/chhs/UA_21/vpmlog.zip
# rm $path2/chhs/UA_21/dpmlog.zip
# rm $path2/chhs/UA_21/vpmlog.zip
# bash /home/ztc/code/getlogDaily/loginmd.sh $path2/chhs/UA_21 $des_date 1 UA_21 $cur_time chhs

# echo "child_hosp_lower_vpm_19"
# ssh magicdepth@10.18.0.50 "cd /home/magicdepth/ztc/;bash getlog.sh"
# scp magicdepth@10.18.0.50:/home/magicdepth/ztc/dpmlog.zip $path2/chhs/LA_19
# scp magicdepth@10.18.0.50:/home/magicdepth/ztc/vpmlog.zip $path2/chhs/LA_19
# scp $path2/chhs/LA_19/dpmlog.zip $path1/chhs/LA_19
# scp $path2/chhs/LA_19/vpmlog.zip $path1/chhs/LA_19
# unzip -d $path2/chhs/LA_19 $path2/chhs/LA_19/dpmlog.zip
# unzip -d $path2/chhs/LA_19 $path2/chhs/LA_19/vpmlog.zip
# rm $path2/chhs/LA_19/dpmlog.zip
# rm $path2/chhs/LA_19/vpmlog.zip
bash /home/ztc/code/getlogDaily/loginmd.sh $path2/chhs/LA_19 $des_date 1 LA_19 $cur_time chhs

# echo "child_hosp_lower_vpm_17"
# ssh child_hosp_lower_vpm_17 "cd /home/magicdepth/ztc/;bash getlog.sh"
# scp child_hosp_lower_vpm_17:/home/magicdepth/ztc/dpmlog.zip $path2/chhs/LB_17
# scp child_hosp_lower_vpm_17:/home/magicdepth/ztc/vpmlog.zip $path2/chhs/LB_17
# scp $path2/chhs/LB_17/dpmlog.zip $path1/chhs/LB_17
# scp $path2/chhs/LB_17/vpmlog.zip $path1/chhs/LB_17
# unzip -d $path2/chhs/LB_17 $path2/chhs/LB_17/dpmlog.zip
# unzip -d $path2/chhs/LB_17 $path2/chhs/LB_17/vpmlog.zip
# rm $path2/chhs/LB_17/dpmlog.zip
# rm $path2/chhs/LB_17/vpmlog.zip
# bash /home/ztc/code/getlogDaily/loginmd.sh $path2/chhs/LB_17 $des_date 1 LB_17 $cur_time chhs





# echo "child_hosp_upper_vpm_28"
# ssh child_hosp_upper_vpm_28 "cd /home/magicdepth/ztc/;bash getlog.sh"
# scp child_hosp_upper_vpm_28:/home/magicdepth/ztc/dpmlog.zip $path2/chhs/UB_28
# scp child_hosp_upper_vpm_28:/home/magicdepth/ztc/vpmlog.zip $path2/chhs/UB_28
# scp $path2/chhs/UB_28/dpmlog.zip $path1/chhs/UB_28
# scp $path2/chhs/UB_28/vpmlog.zip $path1/chhs/UB_28
# unzip -d $path2/chhs/UB_28 $path2/chhs/UB_28/dpmlog.zip
# unzip -d $path2/chhs/UB_28 $path2/chhs/UB_28/vpmlog.zip
# rm $path2/chhs/UB_28/dpmlog.zip
# rm $path2/chhs/UB_28/vpmlog.zip
# bash /home/ztc/code/getlogDaily/loginmd.sh $path2/chhs/UB_28 $des_date 1 UB_28 $cur_time chhs


# echo "metro_city_vpm_48"
# ssh metro_city_vpm_48 "cd /home/magicdepth/ztc/;bash getlog.sh"
# scp metro_city_vpm_48:/home/magicdepth/ztc/dpmlog.zip $path2/mtc/LA_48
# scp metro_city_vpm_48:/home/magicdepth/ztc/vpmlog.zip $path2/mtc/LA_48
# scp $path2/mtc/LA_48/dpmlog.zip $path1/mtc/LA_48
# scp $path2/mtc/LA_48/vpmlog.zip $path1/mtc/LA_48
# unzip -d $path2/mtc/LA_48 $path2/mtc/LA_48/dpmlog.zip
# unzip -d $path2/mtc/LA_48 $path2/mtc/LA_48/vpmlog.zip
# rm $path2/mtc/LA_48/dpmlog.zip
# rm $path2/mtc/LA_48/vpmlog.zip
# bash /home/ztc/code/getlogDaily/log.sh $path2/mtc/LA_48 $des_date $des_time LA_48

# echo "metro_city_vpm_49"
# ssh metro_city_vpm_49 "cd /home/magicdepth/ztc/;bash getlog.sh"
# scp metro_city_vpm_49:/home/magicdepth/ztc/dpmlog.zip $path2/mtc/LB_49
# scp metro_city_vpm_49:/home/magicdepth/ztc/vpmlog.zip $path2/mtc/LB_49
# scp $path2/mtc/LB_49/dpmlog.zip $path1/mtc/LB_49
# scp $path2/mtc/LB_49/vpmlog.zip $path1/mtc/LB_49
# unzip -d $path2/mtc/LB_49 $path2/mtc/LB_49/dpmlog.zip
# unzip -d $path2/mtc/LB_49 $path2/mtc/LB_49/vpmlog.zip
# rm $path2/mtc/LB_49/dpmlog.zip
# rm $path2/mtc/LB_49/vpmlog.zip
# bash /home/ztc/code/getlogDaily/log.sh $path2/mtc/LB_49 $des_date $des_time LB_49

# echo "metro_city_vpm_50"
# ssh metro_city_vpm_50 "cd /home/magicdepth/ztc/;bash getlog.sh"
# scp metro_city_vpm_50:/home/magicdepth/ztc/dpmlog.zip $path2/mtc/UA_50
# scp metro_city_vpm_50:/home/magicdepth/ztc/vpmlog.zip $path2/mtc/UA_50
# scp $path2/mtc/UA_50/dpmlog.zip $path1/mtc/UA_50
# scp $path2/mtc/UA_50/vpmlog.zip $path1/mtc/UA_50
# unzip -d $path2/mtc/UA_50 $path2/mtc/UA_50/dpmlog.zip
# unzip -d $path2/mtc/UA_50 $path2/mtc/UA_50/vpmlog.zip
# rm $path2/mtc/UA_50/dpmlog.zip
# rm $path2/mtc/UA_50/vpmlog.zip
# bash /home/ztc/code/getlogDaily/log.sh $path2/mtc/UA_50 $des_date $des_time UA_50

# echo "metro_city_vpm_47"
# ssh metro_city_vpm_47 "cd /home/magicdepth/ztc/;bash getlog.sh"
# scp metro_city_vpm_47:/home/magicdepth/ztc/dpmlog.zip $path2/mtc/UB_47
# scp metro_city_vpm_47:/home/magicdepth/ztc/vpmlog.zip $path2/mtc/UB_47
# scp $path2/mtc/UB_47/dpmlog.zip $path1/mtc/UB_47
# scp $path2/mtc/UB_47/vpmlog.zip $path1/mtc/UB_47
# unzip -d $path2/mtc/UB_47 $path2/mtc/UB_47/dpmlog.zip
# unzip -d $path2/mtc/UB_47 $path2/mtc/UB_47/vpmlog.zip
# rm $path2/mtc/UB_47/dpmlog.zip
# rm $path2/mtc/UB_47/vpmlog.zip
# bash /home/ztc/code/getlogDaily/log.sh $path2/mtc/UB_47 $des_date $des_time UB_47



# echo "kone_upper_vpm_51"
# ssh kone_upper_vpm_51 "cd /home/magicdepth/ztc/;bash getlog.sh"
# scp kone_upper_vpm_51:/home/magicdepth/ztc/dpmlog.zip $path2/kone/LA_51
# scp kone_upper_vpm_51:/home/magicdepth/ztc/vpmlog.zip $path2/kone/LA_51
# scp $path2/kone/LA_51/dpmlog.zip $path1/kone/LA_51
# scp $path2/kone/LA_51/vpmlog.zip $path1/kone/LA_51
# unzip -d $path2/kone/LA_51 $path2/kone/LA_51/dpmlog.zip
# unzip -d $path2/kone/LA_51 $path2/kone/LA_51/vpmlog.zip
# rm $path2/kone/LA_51/dpmlog.zip
# rm $path2/kone/LA_51/vpmlog.zip
# bash /home/ztc/code/getlogDaily/log.sh $path2/kone/LA_51 $des_date $des_time LA_51

# echo "kone_upper_vpm_55"
# ssh kone_upper_vpm_55 "cd /home/magicdepth/ztc/;bash getlog.sh"
# scp kone_upper_vpm_55:/home/magicdepth/ztc/dpmlog.zip $path2/kone/LB_55
# scp kone_upper_vpm_55:/home/magicdepth/ztc/vpmlog.zip $path2/kone/LB_55
# scp $path2/kone/LB_55/dpmlog.zip $path1/kone/LB_55
# scp $path2/kone/LB_55/vpmlog.zip $path1/kone/LB_55
# unzip -d $path2/kone/LB_55 $path2/kone/LB_55/dpmlog.zip
# unzip -d $path2/kone/LB_55 $path2/kone/LB_55/vpmlog.zip
# rm $path2/kone/LB_55/dpmlog.zip
# rm $path2/kone/LB_55/vpmlog.zip
# bash /home/ztc/code/getlogDaily/log.sh $path2/kone/LB_55 $des_date $des_time LB_55
