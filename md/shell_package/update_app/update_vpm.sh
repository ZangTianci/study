#!/bin/bash

path=$1
filename=$2
app=$3

# 判断是否输入3个参数
if [ -z "$3" ] ; then

    echo -e "\nPlease call '$0 <argument>' to run this command!"
    echo "The parameters you entered are $#."
    echo "Please enter three parameters:"
    echo "1.The path of the file to be updated;"
    echo "2.Documents to be updated;"
    echo "3.App name to be updated: gdpm/vpm."
    exit 1
fi

scp -r "ubuntu@150.158.53.110:/home/ubuntu/mddata/static/$filename.tar.gz" "$path"
tar zxvf "$path/$filename.tar.gz" -C "$path"
cp -r "$path/$filename" /opt/vpm/base/
