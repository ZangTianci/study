#!/bin/bash

# 获取当前工作目录
work_dir=$(cd `dirname $0`; pwd)
AppName="gdpm"

appInfo=$(ps -eo pid,comm | awk '{if($2 == "'${AppName}'") print $1 }')
if [ -z "${appInfo}" ]
then
      echo "0"
else
      echo "${appInfo}"
fi
exit 0