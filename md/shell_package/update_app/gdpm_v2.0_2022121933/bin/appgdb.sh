#!/bin/bash

# 获取当前工作目录
work_dir=$(cd `dirname $0`; pwd)
AppName="gdpm"

export MDNotDeamon=1
export LD_LIBRARY_PATH=.:${work_dir}:${work_dir}/../userlib:${work_dir}/../syslib

pid=`${work_dir}/appmonitor.sh`
if [ ${pid} -ne 0 ]; then
   echo "${AppName} repeat run"
   exit 1
fi

gdb ${work_dir}/${AppName}
