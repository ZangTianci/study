#!/bin/bash

path=$1
filename=$2
app=$3

# 判断是否输入3个参数
if [ -z "$3" ]; then

    echo -e "\nPlease call '$0 <argument>' to run this command!"
    echo "The parameters you entered are $#."
    echo "Please enter three parameters:"
    echo "1.The path of the file to be updated;"
    echo "2.Documents to be updated;"
    echo "3.App name to be updated: gdpm/vpm."
    exit 1
fi

# 判断path末尾是否以/结尾，否则加上/，再拼接filename
if echo "$path"|grep -q -E '\/$';then
    filepath="$path$filename"
else
    filepath="$path/$filename"
fi

for file_a in ${filepath}/*
do
    temp_file=`basename $file_a`
    if echo "$temp_file"|grep -q -E '\gz$';then
        temp_file=`basename $temp_file .tar.gz`
        if echo "$temp_file"|grep -q -E '^daemon*';then
            daemon_file=$temp_file
        elif echo "$temp_file"|grep -q -E '^vpm*'||echo "$temp_file"|grep -q -E '^gdpm*';then
            app_file=$temp_file
        fi
    fi
done

if  [ -e "$filepath/$daemon_file.tar.gz" ] ;then
    mkdir "$filepath/$daemon_file"
    tar zxvf "$filepath/$daemon_file.tar.gz" -C "$filepath/$daemon_file"
    rm -rf $filepath/$daemon_file/daemon.json
    rm -rf $filepath/$daemon_file.tar.gz
    cd "$filepath"
    tar zcvf "$daemon_file.tar.gz" "$daemon_file/"
    scp -r "$filepath/$daemon_file.tar.gz" ubuntu@150.158.53.110:/home/ubuntu/mddata/static/
fi

if [ -e "$filepath/$app_file.tar.gz" ] ;then
    mkdir "$filepath/$app_file"
    tar zxvf "$filepath/$app_file.tar.gz" -C "$filepath/$app_file"
    rm -rf $filepath/$app_file/config
    rm -rf $filepath/$app_file.tar.gz
    cd "$filepath"
    tar zcvf "$app_file.tar.gz" "$app_file/"
    scp -r "$filepath/$app_file.tar.gz" ubuntu@150.158.53.110:/home/ubuntu/mddata/static/
fi



if [ $app = "vpm" ]; then
    echo "vpm"
elif [ $app = "gdpm" ]; then
    echo "gdpm"
fi