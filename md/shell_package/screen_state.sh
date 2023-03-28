#!/bin/bash
export DISPLAY=:0.0
screen_info=`xrandr`
error_info="HDMI-1 disconnected"
if [[ $screen_info =~ $error_info ]];then
    echo "HDMI未连接"
else
    echo "HDMI已连接"
fi
