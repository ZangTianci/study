#!/bin/bash

# 获取当前工作目录
work_dir=$(cd `dirname $0`; pwd)
AppName="gdpm"

export LD_LIBRARY_PATH=.:${work_dir}:${work_dir}/../userlib:${work_dir}/../syslib

if [ ! -d "/data/corefile" ];then
    mkdir /data/corefile
fi

#默认开启core 默认core最大大小1G
echo "/data/corefile/%e.core"> /proc/sys/kernel/core_pattern
ulimit -c 1073741824

pid=`${work_dir}/appmonitor.sh`
if [ ${pid} -ne 0 ]; then
   echo "${AppName} repeat run"
   exit 1
fi

${work_dir}/${AppName}

echo "${AppName} start"

exit 0