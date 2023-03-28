#!/bin/bash
set -o errexit

vsm_ip=$1
dest_dir=$2

if [[ -z $vsm_ip || -z $dest_dir ]];then
  exit 1
fi

# 定义
vsm_src_dir=/system/etc

# 断开所有连接
adb disconnect

# 连接VSM
adb connect $vsm_ip

# 拉取文件
adb pull $vsm_src_dir/axis.yml $dest_dir
adb pull $vsm_src_dir/axis_forward.yml $dest_dir
adb pull $vsm_src_dir/parameters.xml $dest_dir

# 断开连接
adb disconnect

exit 0
